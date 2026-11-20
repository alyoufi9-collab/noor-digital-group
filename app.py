# Noor Digital Group - Backend - جديد - FastAPI - من الصفر
import os, re, uuid
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import FastAPI, Depends, HTTPException, status, WebSocket, WebSocketDisconnect, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, Field, EmailStr, field_validator
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, Session
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from .models import Base, User, UserRole, AdCampaign, CampaignStatus, AdObjective, SavedAudience, AdSchedule, AdPlacementSetting, WalletTopup

# --- اعدادات ---
SECRET_KEY = os.getenv("SECRET_KEY", "noor-secret-change-this-in-render-123456789")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./noor.db")
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# روابطنا الرسمية فقط - Vercel
ALLOWED_ORIGINS = [
    "https://noorbook.vercel.app",
    "https://noorsocial.vercel.app",
    "https://noorshot.vercel.app",
    "https://noorchat.vercel.app",
    "https://noormarket.vercel.app",
    "http://localhost:3000",
]

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base.metadata.create_all(bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="Noor Digital Group API - جديد")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Security Headers
@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers["Referrer-Policy"] = "no-referrer"
    return response

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- فلترة تلقائية - AI Moderation - جديد ---
BANNED_WORDS = ["قمار", "سحر", "مخدرات", "نصب", "سلاح", "كراهية", "gambling", "casino", "porn", "sex", "drugs", "weapon", "scam", "telegram", "تليجرام"]
def check_moderation(text: str):
    low = (text or "").lower()
    found = [w for w in BANNED_WORDS if w.lower() in low]
    if found:
        raise HTTPException(status_code=400, detail=f"محتوى مخالف: {', '.join(found)} - ممنوع في مجموعة نور")
    # منع XSS
    if "<script" in low or "javascript:" in low or "onerror=" in low:
        raise HTTPException(status_code=400, detail="محتوى مخالف - XSS ممنوع")
    return True

# --- Pydantic - تحقق صارم ---
class RegisterIn(BaseModel):
    full_name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    phone: str = Field(min_length=9, max_length=20)
    password: str = Field(min_length=6, max_length=100)
    @field_validator("full_name", "phone", "password")
    @classmethod
    def no_script(cls, v: str):
        if "<" in v or ">" in v:
            raise ValueError("ممنوع رموز HTML")
        return v.strip()

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    full_name: str
    role: str

class CampaignIn(BaseModel):
    title: str = Field(min_length=2, max_length=200)
    text: str = Field(default="", max_length=2000)
    objective: str = Field(default="traffic")
    daily_budget: int = Field(default=0, ge=0)
    lifetime_budget: int = Field(default=0, ge=0)
    budget_type: str = Field(default="daily")

class CampaignOut(BaseModel):
    id: str
    title: str
    objective: str
    status: str
    daily_budget: int
    spend: int
    reach: int
    clicks: int
    sales: int
    revenue: int
    cpm: float
    cpc: float
    cpa: float

# --- Auth - SSO ---
def verify_password(plain: str, hashed: str):
    return pwd_context.verify(plain, hashed)

def get_password_hash(p: str):
    return pwd_context.hash(p)

def create_token(user_id: str):
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode({"sub": user_id, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        uid = payload.get("sub")
        if not uid:
            raise HTTPException(status_code=401, detail="توكن غير صالح")
    except JWTError:
        raise HTTPException(status_code=401, detail="توكن غير صالح")
    user = db.scalar(select(User).where(User.id == uuid.UUID(uid)))
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="مستخدم غير موجود")
    return user

# --- WebSocket - دردشة فورية ---
class ConnectionManager:
    def __init__(self):
        self.active: dict[str, list[WebSocket]] = {}
    async def connect(self, ws: WebSocket, room: str):
        await ws.accept()
        self.active.setdefault(room, []).append(ws)
    def disconnect(self, ws: WebSocket, room: str):
        if room in self.active and ws in self.active[room]:
            self.active[room].remove(ws)
    async def broadcast(self, room: str, message: dict):
        for ws in self.active.get(room, []):
            try:
                await ws.send_json(message)
            except:
                pass

manager = ConnectionManager()

@app.websocket("/ws/chat/{room}")
async def ws_chat(ws: WebSocket, room: str):
    await manager.connect(ws, room)
    try:
        while True:
            data = await ws.receive_json()
            text = str(data.get("text", ""))[:2000]
            check_moderation(text)
            await manager.broadcast(room, {"room": room, "user": data.get("user", "ضيف"), "text": text, "type": data.get("type", "message")})
    except WebSocketDisconnect:
        manager.disconnect(ws, room)
    except Exception:
        manager.disconnect(ws, room)

# --- Routes ---
@app.get("/")
def root():
    return {"app": "Noor Digital Group API - جديد", "status": "ok", "version": "V1-new"}

@app.post("/auth/register", response_model=TokenOut)
@limiter.limit("5/minute")
def register(request: Request, body: RegisterIn, db: Session = Depends(get_db)):
    check_moderation(body.full_name)
    exists = db.scalar(select(User).where((User.email == body.email) | (User.phone == body.phone)))
    if exists:
        raise HTTPException(status_code=400, detail="البريد او الجوال مسجل من قبل")
    is_first = db.scalar(select(User)) is None
    user = User(full_name=body.full_name, email=body.email.lower(), phone=body.phone, hashed_password=get_password_hash(body.password), role=UserRole.ADMIN if is_first else UserRole.USER)
    db.add(user)
    db.commit()
    db.refresh(user)
    return TokenOut(access_token=create_token(str(user.id)), user_id=str(user.id), full_name=user.full_name, role=user.role.value)

@app.post("/auth/login", response_model=TokenOut)
@limiter.limit("5/minute")
def login(request: Request, form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # SSO - دخول بالبريد او الجوال
    user = db.scalar(select(User).where((User.email == form.username.lower()) | (User.phone == form.username)))
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="بيانات غلط")
    return TokenOut(access_token=create_token(str(user.id)), user_id=str(user.id), full_name=user.full_name, role=user.role.value)

@app.get("/auth/me")
def me(user: User = Depends(get_current_user)):
    return {"id": str(user.id), "full_name": user.full_name, "email": user.email, "phone": user.phone, "role": user.role.value, "balance": user.balance}

# --- Objectives - من كراسك ---
NOOR_OBJECTIVES = {
    "awareness": {"ar": "وعي", "en": "Awareness", "desc": "الوصول الى الاشخاص الاكثر احتمالا لمشاهدة فيديوك"},
    "traffic": {"ar": "زيارات", "en": "Traffic", "desc": "توجيه الاشخاص الى وجهة مثل موقعك او تطبيقك او حدث نور"},
    "engagement": {"ar": "تفاعل", "en": "Engagement", "desc": "زيادة الرسائل - مشاهدات الفيديو - التفاعل مع المنشورات - الاعجاب بالصفحة", "good_for": "نور شات و نور توك"},
    "leads": {"ar": "عملاء محتملين", "en": "Leads", "desc": "جمع العملاء المحتملين لعلامتك التجارية"},
    "sales": {"ar": "مبيعات", "en": "Sales", "desc": "جعل الناس يشاهدون المحتوى - يتصلون بالعمل - يضيفون الى قائمة الامنيات"},
    "calls": {"ar": "مكالمات", "en": "Calls", "desc": "جلب الاشخاص المهتمين بعملك ليتصلوا بك"},
}

@app.get("/api/ads/objectives")
def get_objectives():
    return NOOR_OBJECTIVES

# --- Campaigns + Auction ---
@app.post("/api/ads/campaigns", response_model=CampaignOut)
@limiter.limit("20/minute")
def create_campaign(request: Request, body: CampaignIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    check_moderation(body.title + " " + body.text)
    # محرك المزاد - Ad Score = Bid x Quality x Relevance
    bid = 50.0
    quality = 0.9
    relevance = 0.8
    my_score = bid * quality * relevance
    second_score = 32.0
    cpm = (second_score / (quality * relevance)) + 0.01
    cpc = cpm / (0.02 * 10)
    cpa = cpc / 0.07
    spend = body.daily_budget if body.budget_type == "daily" else body.lifetime_budget
    if spend > 0 and spend > user.balance:
        raise HTTPException(status_code=400, detail=f"رصيدك {user.balance} - ما كافي")
    if spend > 0:
        user.balance -= spend
    reach = int(spend * 0.2) if spend > 0 else 1000
    sales = int(reach * 0.007) if reach > 0 else 7
    revenue = sales * 3200
    camp = AdCampaign(user_id=user.id, title=body.title, text=body.text, objective=AdObjective(body.objective) if body.objective in [e.value for e in AdObjective] else AdObjective.TRAFFIC, daily_budget=body.daily_budget, lifetime_budget=body.lifetime_budget, budget_type=body.budget_type, spend=spend, reach=reach, clicks=int(reach*0.02), sales=sales, revenue=revenue, cpm=cpm, cpc=cpc, cpa=cpa, status=CampaignStatus.PENDING)
    db.add(camp)
    db.commit()
    db.refresh(camp)
    return CampaignOut(id=str(camp.id), title=camp.title, objective=camp.objective.value, status=camp.status.value, daily_budget=camp.daily_budget, spend=camp.spend, reach=camp.reach, clicks=camp.clicks, sales=camp.sales, revenue=camp.revenue, cpm=float(camp.cpm), cpc=float(camp.cpc), cpa=float(camp.cpa))

@app.get("/api/ads/campaigns")
def list_campaigns(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    camps = db.scalars(select(AdCampaign).where(AdCampaign.user_id == user.id).order_by(AdCampaign.created_at.desc())).all()
    return [{"id": str(c.id), "title": c.title, "objective": c.objective.value, "status": c.status.value, "daily_budget": c.daily_budget, "spend": c.spend, "reach": c.reach, "clicks": c.clicks, "sales": c.sales, "revenue": c.revenue, "cpm": float(c.cpm), "cpc": float(c.cpc), "cpa": float(c.cpa)} for c in camps]

# --- Wallet ---
@app.post("/api/wallet/topup")
def topup(body: dict, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    amount = int(body.get("amount", 0))
    method = str(body.get("method", "bankak"))
    if amount < 1000:
        raise HTTPException(status_code=400, detail="اقل شحن 1000")
    t = WalletTopup(user_id=user.id, amount=amount, method=method, reference=str(body.get("reference", "")), status="pending")
    db.add(t)
    db.commit()
    return {"ok": True, "msg": "تم ارسال طلب الشحن - الادمن ح يوافق", "id": str(t.id)}

@app.post("/api/wallet/approve/{topup_id}")
def approve_topup(topup_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="ادمن بس")
    t = db.scalar(select(WalletTopup).where(WalletTopup.id == uuid.UUID(topup_id)))
    if not t:
        raise HTTPException(status_code=404, detail="ما لقينا الطلب")
    if t.status == "approved":
        return {"ok": True, "msg": "تمت الموافقة من قبل"}
    t.status = "approved"
    owner = db.scalar(select(User).where(User.id == t.user_id))
    owner.balance += t.amount
    db.commit()
    return {"ok": True, "msg": f"تم شحن {t.amount} للمستخدم"}
