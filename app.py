# NoorBook V31 - Noor Digital Group - NoorBook Ads Manager
# اسماء نور بس - ما فيهو Facebook / Messenger / WhatsApp / Meta / Instagram
# انشاء حملة = 3 خطوات موبايل: 1- Campaign  2- Ad Sets (مجموعات)  3- Ad
# 6 اهداف - تحديث ميتا الاخير - + جدولة باليوم والساعة + ميزانية + محفظة + AI

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import json, uuid, datetime

app = FastAPI(title="NoorBook - Noor Digital Group")

# ===== قاعدة بيانات مؤقتة في الذاكرة - بعدين بنربطها بقاعدة حقيقية =====
DB = {"campaigns": [], "adsets": [], "ads": [], "wallet": 50000}

# ===== موديلات البيانات =====
class Campaign(BaseModel):
    name: str
    objective: str  # AWARENESS / TRAFFIC / ENGAGEMENT / LEADS / APP / SALES
    budget_type: str = "lifetime"  # lifetime / daily
    budget: float = 10000
    ab_test: bool = False
    advantage_budget: bool = True
    status: str = "ACTIVE"

class AdSet(BaseModel):
    campaign_id: str
    name: str
    audience_age_min: int = 18
    audience_age_max: int = 65
    audience_gender: str = "all"  # all / male / female
    location: str = "السودان - الخرطوم"
    interests: str = ""
    budget: float = 5000
    # الجدولة - Schedule
    schedule_type: str = "continuous"  # continuous / scheduled
    start_date: str = ""
    end_date: str = ""
    timezone: str = "Africa/Khartoum"
    # جدول الاسبوع: 7 ايام - كل يوم: {day, enabled, from_hour, to_hour}
    week_schedule: List[dict] = []
    placements: List[str] = ["NoorSocial Feed", "NoorShot Reels", "NoorChat"]
    performance_goal: str = ""
    status: str = "ACTIVE"

class Ad(BaseModel):
    adset_id: str
    name: str
    headline: str
    primary_text: str
    cta: str = "اعرف المزيد"
    media_url: str = ""
    destination: str = ""

# ===== الصفحة الرئيسية - الواجهة - موبايل - عصري - اسود + ذهبي =====
HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>NoorBook - مدير اعلانات نور</title>
<style>
*{box-sizing:border-box;font-family:system-ui,-apple-system,sans-serif}
body{margin:0;background:#0A0A0A;color:#fff;padding-bottom:90px}
.top{position:sticky;top:0;background:#111;padding:14px 16px;display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #222;z-index:10}
.logo{font-weight:900;font-size:22px}.logo span{color:#F5C518}
.wallet{background:#1A1A1A;border:1px solid #333;padding:8px 12px;border-radius:999px;font-size:13px}
.wallet b{color:#F5C518}
.steps{display:flex;gap:8px;padding:14px 16px}
.step{flex:1;text-align:center;background:#1A1A1A;padding:10px 4px;border-radius:12px;font-size:12px;border:1px solid #222}
.step.active{background:#F5C518;color:#000;font-weight:800}
.card{background:#151515;border:1px solid #222;border-radius:16px;padding:14px;margin:12px 16px}
.card h3{margin:0 0 8px}.muted{color:#aaa;font-size:13px;line-height:1.6}
label{display:block;font-size:13px;margin:12px 0 6px;color:#ddd}
input,select,textarea{width:100%;background:#1E1E1E;border:1px solid #333;color:#fff;padding:12px;border-radius:12px;font-size:15px}
textarea{min-height:70px}
.obj-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.obj{border:2px solid #2A2A2A;background:#1A1A1A;padding:12px;border-radius:14px;cursor:pointer}
.obj.selected{border-color:#F5C518;background:#241F08}
.obj b{display:block}.obj small{color:#aaa;line-height:1.5;display:block;margin-top:4px}
.obj .algo{font-size:11px;color:#F5C518;margin-top:6px}
.row{display:flex;gap:10px}.row>*{flex:1}
.week-day{background:#1E1E1E;border:1px solid #2A2A2A;border-radius:12px;padding:10px;margin-top:10px}
.week-day .head{display:flex;justify-content:space-between;align-items:center}
.btn{width:100%;background:#F5C518;color:#000;border:0;padding:14px;border-radius:14px;font-weight:900;font-size:16px;margin-top:14px}
.btn2{background:#222;color:#fff;border:1px solid #333;padding:10px 14px;border-radius:10px}
.chip{display:inline-block;background:#222;border:1px solid #333;padding:6px 10px;border-radius:999px;font-size:12px;margin:4px 4px 0 0}
.nav{position:fixed;bottom:0;right:0;left:0;background:#111;border-top:1px solid #222;display:flex;padding:10px}
.nav div{flex:1;text-align:center;font-size:12px;color:#aaa}.nav div.on{color:#F5C518;font-weight:800}
.hide{display:none}
.kpi{display:flex;gap:10px}.kpi div{flex:1;background:#1E1E1E;border-radius:14px;padding:12px;text-align:center}.kpi b{font-size:18px;color:#F5C518}
</style>
</head>
<body>
<div class="top"><div class="logo">N <span>NoorBook</span></div><div class="wallet">المحفظة: <b id="walletVal">50,000</b> ج.س</div></div>

<!-- لوحة المعلومات -->
<div class="card"><h3>👋 اهلا بيك في NoorBook</h3><p class="muted">مدير اعلانات نور - زي ميتا بالظبط - بس باسماء وشعارات نور - 3 مستويات: حملة &gt; مجموعات &gt; اعلان</p>
<div class="kpi"><div><b id="kCamp">0</b><br><small>حملة</small></div><div><b id="kSet">0</b><br><small>مجموعة</small></div><div><b id="kAd">0</b><br><small>اعلان</small></div></div>
</div>

<!-- الخطوات -->
<div class="steps">
<div class="step active" id="s1">1 - الحملة<br>Campaign</div>
<div class="step" id="s2">2 - المجموعات<br>Ad Sets</div>
<div class="step" id="s3">3 - الاعلان<br>Ad</div>
</div>

<!-- الخطوة 1 -->
<div id="page1">
<div class="card"><h3>1 - انشاء الحملة - Campaign</h3><p class="muted">اختار الهدف - الهدف بيقول للخوارزمية تدور على منو. لو اخترت غلط - حتجيب ليك ناس غلط.</p>
<label>اسم الحملة</label><input id="campName" placeholder="مثال: عطور عطبرة - رمضان">
<label>اختر هدف الحملة - 6 اهداف - تحديث ميتا الاخير</label>
<div class="obj-grid" id="objs"></div>
<label>نوع الميزانية</label>
<select id="budgetType"><option value="lifetime">ميزانية مدى الحياة - Lifetime - لازم للجدولة</option><option value="daily">ميزانية يومية - Daily</option></select>
<label>ميزانية الحملة الكلية (ج.س)</label><input id="campBudget" type="number" value="50000">
<label><input type="checkbox" id="abTest"> اختبار A/B - جرب اعلانين وشوف الاحسن</label>
<label><input type="checkbox" id="advBudget" checked> Advantage Campaign Budget - خلي الخوارزمية توزع الميزانية</label>
<button class="btn" onclick="go2()">التالي - المجموعات →</button>
</div>
</div>

<!-- الخطوة 2 -->
<div id="page2" class="hide">
<div class="card"><h3>2 - مجموعات الاعلانات - Ad Sets</h3><p class="muted">جوه نفس الحملة - اعمل اكتر من مجموعة - كل مجموعة جمهور براهو - وميزانية براها - وجدول براهو - والخوارزمية حتختار الاحسن.</p>
<div id="setsList"></div>
<button class="btn2" onclick="addSetUI()">+ اضافة مجموعة جديدة</button>
<div id="setForm"></div>
<button class="btn" onclick="go3()">التالي - الاعلان →</button>
<button class="btn2" style="width:100%;margin-top:10px" onclick="go1()">← رجوع</button>
</div>
</div>

<!-- الخطوة 3 -->
<div id="page3" class="hide">
<div class="card"><h3>3 - الاعلان - Ad</h3><p class="muted">ده البشوفو الزبون في NoorSocial و NoorShot و NoorChat</p>
<label>اسم الاعلان</label><input id="adName" placeholder="اعلان 1 - فيديو عطور">
<label>العنوان الرئيسي Headline</label><input id="adHead" placeholder="عطور اصلية - توصيل عطبرة">
<label>النص الاساسي Primary Text</label><textarea id="adText" placeholder="اكتب نص يجذب العميل المهتم - ما الفضولي..."></textarea>
<label>زر الدعوة CTA</label><select id="adCta"><option>اعرف المزيد</option><option>تسوق الان</option><option>ارسل رسالة - NoorChat</option><option>اتصل - NoorTalk</option><option>حمّل التطبيق</option><option>سجّل الان</option></select>
<label>رابط الصورة / الفيديو</label><input id="adMedia" placeholder="https://...">
<label>وجهة الاعلان - وين يمشي الزبون؟</label><select id="adDest"><option>NoorSocial - صفحة</option><option>NoorMarket - متجر</option><option>NoorChat - دردشة</option><option>NoorTalk - مكالمة</option><option>موقع خارجي</option></select>
<div class="card" style="margin:12px 0"><b>معاينة - Preview</b><p class="muted" id="preview">...</p></div>
<button class="btn" onclick="publish()">🚀 نشر الحملة - Publish</button>
<button class="btn2" style="width:100%;margin-top:10px" onclick="go2()">← رجوع</button>
</div>
</div>

<!-- قائمة الحملات -->
<div class="card"><h3>📋 حملاتي</h3><div id="myCamps"><p class="muted">لسه ما عملت حملة - اعمل اول حملة فوق</p></div></div>

<div class="nav"><div class="on">🏠 الرئيسية</div><div onclick="go1()">📢 حملات</div><div>👥 جمهور</div><div>💰 محفظة</div><div>🤖 Noor AI</div></div>

<script>
const OBJECTIVES=[
{id:'AWARENESS',t:'الوعي - Awareness',d:'ناس تتذكر اعلانك',algo:'الخوارزمية: تدور على ناس بتتذكر - Reach + Recall'},
{id:'TRAFFIC',t:'الزيارات - Traffic',d:'ناس تدوس على اللينك',algo:'الخوارزمية: تدور على ناس بتدوس - Link Click'},
{id:'ENGAGEMENT',t:'التفاعل - Engagement',d:'لايك - تعليق - شير - مشاهدة',algo:'الخوارزمية: تدور على ناس بتتفاعل'},
{id:'LEADS',t:'العملاء المحتملين - Leads',d:'فورم - اتصال - رسالة جادة',algo:'الخوارزمية: تدور على ناس بتملا بيانات'},
{id:'APP',t:'ترويج التطبيق - App',d:'تحميل التطبيق',algo:'الخوارزمية: تدور على ناس بتنزل تطبيقات'},
{id:'SALES',t:'المبيعات - Sales',d:'شراء - اضافة للسلة',algo:'الخوارزمية: تدور على ناس بتشتري - لازم Noor Pixel شغال'},
];
let selObj='SALES'; let sets=[];
const DAYS=['السبت','الاحد','الاثنين','الثلاثاء','الاربعاء','الخميس','الجمعة'];
function renderObjs(){document.getElementById('objs').innerHTML=OBJECTIVES.map(o=>`<div class="obj ${o.id==selObj?'selected':''}" onclick="selObj='${o.id}';renderObjs()"><b>${o.t}</b><small>${o.d}</small><div class="algo">${o.algo}</div></div>`).join('')}
renderObjs();
function go1(){show(1)} function go2(){if(!document.getElementById('campName').value){alert('اكتب اسم الحملة اول');return} show(2); if(sets.length==0) addSetUI()} function go3(){show(3); updatePreview()}
function show(n){[1,2,3].forEach(i=>{document.getElementById('page'+i).classList.toggle('hide',i!==n); document.getElementById('s'+i).classList.toggle('active',i===n)})}
function defaultWeek(){return DAYS.map(d=>({day:d,enabled:true,from:'09:00',to:'23:00'}))}
function addSetUI(){sets.push({name:'مجموعة '+(sets.length+1),location:'السودان - الخرطوم',age_min:18,age_max:65,gender:'all',budget:10000,schedule_type:'continuous',start:'',end:'',week:defaultWeek(),placements:['NoorSocial Feed']}); renderSets()}
function renderSets(){
document.getElementById('setsList').innerHTML=sets.map((s,i)=>`<div class="chip">📁 ${s.name} - ${s.location} - ${s.budget} ج.س</div>`).join('');
let s=sets[sets.length-1]; if(!s) return;
document.getElementById('setForm').innerHTML=`
<label>اسم المجموعة ${sets.length}</label><input value="${s.name}" onchange="sets[${sets.length-1}].name=this.value;renderSets()">
<div class="row"><div><label>العمر من</label><input type="number" value="${s.age_min}" onchange="sets[${sets.length-1}].age_min=this.value"></div><div><label>العمر لي</label><input type="number" value="${s.age_max}" onchange="sets[${sets.length-1}].age_max=this.value"></div></div>
<label>الجنس</label><select onchange="sets[${sets.length-1}].gender=this.value"><option value="all">الكل</option><option value="male">رجال</option><option value="female">نساء</option></select>
<label>الموقع - Location</label><input value="${s.location}" onchange="sets[${sets.length-1}].location=this.value">
<label>الاهتمامات</label><input placeholder="عطور - تجارة - عقارات" onchange="sets[${sets.length-1}].interests=this.value">
<label>ميزانية المجموعة</label><input type="number" value="${s.budget}" onchange="sets[${sets.length-1}].budget=this.value">
<label>اماكن الظهور - Placements</label><div><span class="chip">NoorSocial Feed</span><span class="chip">NoorShot Reels</span><span class="chip">NoorChat</span><span class="chip">NoorMarket</span></div>
<h3 style="margin-top:16px">🗓️ الجدولة - Schedule - متى يظهر الاعلان؟</h3>
<label>نوع التشغيل</label><select onchange="sets[${sets.length-1}].schedule_type=this.value;renderSets()"><option value="continuous">تشغيل مستمر - 24 ساعة</option><option value="scheduled">جدولة - اختار ايام وساعات</option></select>
<div class="row"><div><label>تاريخ البداية</label><input type="date" onchange="sets[${sets.length-1}].start=this.value"></div><div><label>تاريخ النهاية</label><input type="date" onchange="sets[${sets.length-1}].end=this.value"></div></div>
<label>المنطقة الزمنية</label><select><option>Africa/Khartoum - GMT+2 - السودان</option></select>
<div style="display:flex;gap:8px;margin-top:10px"><button class="btn2" onclick="setWeekAll()">كل الاسبوع</button><button class="btn2" onclick="setWeekPeak()">ساعات الذروة 6م-11م</button><button class="btn2" onclick="setWeekWork()">ايام العمل بس</button></div>
<div id="weekBox">${s.week.map((w,wi)=>`<div class="week-day"><div class="head"><b>${w.day}</b><label><input type="checkbox" ${w.enabled?'checked':''} onchange="sets[${sets.length-1}].week[${wi}].enabled=this.checked"> شغال</label></div><div class="row"><div><label>من</label><input type="time" value="${w.from}" onchange="sets[${sets.length-1}].week[${wi}].from=this.value"></div><div><label>لي</label><input type="time" value="${w.to}" onchange="sets[${sets.length-1}].week[${wi}].to=this.value"></div></div></div>`).join('')}</div>
<p class="muted">المعاينة: الاعلان حيظهر ${calcHours(s)} ساعة في الاسبوع - من 168 ساعة</p>
`;
}
function calcHours(s){let h=0; s.week.forEach(w=>{if(!w.enabled) return; let a=parseInt(w.from), b=parseInt(w.to); h+=Math.max(0,b-a)}); return h}
function setWeekAll(){let s=sets[sets.length-1]; s.week=defaultWeek(); renderSets()}
function setWeekPeak(){let s=sets[sets.length-1]; s.week=DAYS.map(d=>({day:d,enabled:true,from:'18:00',to:'23:00'})); renderSets()}
function setWeekWork(){let s=sets[sets.length-1]; s.week=DAYS.map((d,i)=>({day:d,enabled:i<5,from:'09:00',to:'23:00'})); renderSets()}
function updatePreview(){document.getElementById('preview').innerText=(document.getElementById('adHead').value||'العنوان')+' - '+(document.getElementById('adText').value||'النص')+' - زر: '+(document.getElementById('adCta').value)}
document.getElementById('adHead').addEventListener('input',updatePreview); document.getElementById('adText').addEventListener('input',updatePreview);
async function publish(){
let camp={name:document.getElementById('campName').value, objective:selObj, budget_type:document.getElementById('budgetType').value, budget:parseFloat(document.getElementById('campBudget').value||0), ab_test:document.getElementById('abTest').checked, advantage_budget:document.getElementById('advBudget').checked};
let r=await fetch('/api/campaigns',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(camp)}); let c=await r.json();
for(let s of sets){await fetch('/api/adsets',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({campaign_id:c.id,name:s.name,location:s.location,audience_age_min:parseInt(s.age_min),audience_age_max:parseInt(s.age_max),audience_gender:s.gender,budget:parseFloat(s.budget),schedule_type:s.schedule_type,start_date:s.start,end_date:s.end,week_schedule:s.week})})}
alert('✅ تم نشر الحملة - '+c.name+' - الهدف: '+selObj+' - المجموعات: '+sets.length); loadCamps();
}
async function loadCamps(){let r=await fetch('/api/campaigns'); let d=await r.json(); document.getElementById('kCamp').innerText=d.length; document.getElementById('myCamps').innerHTML=d.map(x=>`<div class="chip">📢 ${x.name} - ${x.objective} - ${x.budget} ج.س - ${x.status}</div>`).join('')||'لسه ما عملت حملة'; let r2=await fetch('/api/wallet'); let w=await r2.json(); document.getElementById('walletVal').innerText=w.balance.toLocaleString()}
loadCamps();
</script>
</body></html>
"""

@app.get("/", response_class=HTMLResponse)
def home(): return HTML

@app.get("/api/wallet")
def wallet(): return {"balance": DB["wallet"]}

@app.get("/api/campaigns")
def list_camps(): return DB["campaigns"]

@app.post("/api/campaigns")
def create_camp(c: Campaign):
    d = c.dict(); d["id"] = str(uuid.uuid4())[:8]; d["created_at"] = str(datetime.datetime.now())
    DB["campaigns"].append(d); return d

@app.post("/api/adsets")
def create_set(s: AdSet):
    d = s.dict(); d["id"] = str(uuid.uuid4())[:8]; DB["adsets"].append(d); return d

@app.get("/api/adsets")
def list_sets(): return DB["adsets"]

@app.post("/api/ads")
def create_ad(a: Ad):
    d = a.dict(); d["id"] = str(uuid.uuid4())[:8]; DB["ads"].append(d); return d

@app.get("/api/health")
def health(): return {"ok": True, "app": "NoorBook V31"}
