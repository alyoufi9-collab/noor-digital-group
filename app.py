from flask import Flask, render_template_string, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = "noor-secret-2026"

# بيانات وهمية للتجربة
POSTS = [
    {"user": "نور", "text": "مرحب بيكم في Noor Digital Group 🔥 أكبر منصة سودانية", "likes": 124},
    {"user": "يوسف", "text": "NoorShot نزل - صور فيديو واربح 🔥", "likes": 89},
    {"user": "سارة", "text": "منو جرب NoorMarket ؟ اشتريت منو امبارح والله رهيب", "likes": 56},
]
PRODUCTS = [
    {"name": "تلفون سامسونج", "price": "450,000 ج", "img": "📱"},
    {"name": "لابتوب HP", "price": "1,200,000 ج", "img": "💻"},
    {"name": "سماعة بلوتوث", "price": "85,000 ج", "img": "🎧"},
    {"name": "ساعة ذكية", "price": "120,000 ج", "img": "⌚"},
]
VIDEOS = [
    {"title": "فيديو ترند سوداني 🔥", "user": "@yousuf", "views": "12K"},
    {"title": "تحدي الضحك 😂", "user": "@sara", "views": "8K"},
    {"title": "أغنية جديدة", "user": "@noor", "views": "25K"},
]

BASE_CSS = """
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:'Segoe UI',Tahoma,sans-serif}
body{background:#f0f2f5;direction:rtl}
.top{background:#fff;padding:12px 15px;display:flex;justify-content:space-between;align-items:center;box-shadow:0 2px 10px #0001;position:sticky;top:0;z-index:99}
.logo{font-size:22px;font-weight:900;color:#1877f2}
.logo span{color:#ff6b00}
.top a{color:#333;text-decoration:none;font-weight:700;margin:0 5px;font-size:14px}
.btn{background:#1877f2;color:#fff!important;padding:8px 16px;border-radius:20px}
.hero{background:linear-gradient(135deg,#1877f2,#7b2ff7,#ff6b00);color:#fff;padding:35px 20px;text-align:center}
.hero h1{font-size:28px;margin-bottom:10px}
.hero p{opacity:.9;line-height:1.6}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;padding:15px}
.card{background:#fff;border-radius:16px;padding:18px;text-align:center;box-shadow:0 2px 10px #0001}
.card .icon{font-size:38px;margin-bottom:8px}
.card h3{margin-bottom:5px}
.card p{color:#777;font-size:13px;line-height:1.5;margin-bottom:12px}
.card a{display:block;background:#1877f2;color:#fff;padding:10px;border-radius:10px;text-decoration:none;font-weight:700}
.card:nth-child(2) a{background:#ff6b00}
.card:nth-child(3) a{background:#e1306c}
.card:nth-child(4) a{background:#00c853}
.card:nth-child(5) a{background:#7b2ff7}
.card:nth-child(6) a{background:#111}
.container{max-width:600px;margin:auto;padding:15px}
.post{background:#fff;border-radius:14px;padding:15px;margin-bottom:12px;box-shadow:0 1px 5px #0001}
.post b{font-size:16px}
.post p{margin:10px 0;line-height:1.6}
.actions{display:flex;gap:10px;color:#555;font-size:14px;border-top:1px solid #eee;padding-top:10px}
.product{background:#fff;border-radius:14px;padding:15px;text-align:center;box-shadow:0 1px 5px #0001}
.product .img{font-size:50px}
.product h3{margin:10px 0 5px}
.product .price{color:#00c853;font-weight:900;font-size:18px}
.video{background:#111;color:#fff;border-radius:14px;padding:20px;margin-bottom:12px}
.video h3{margin-bottom:5px}
.video span{color:#aaa;font-size:13px}
.chatbox{background:#fff;border-radius:14px;padding:15px}
.msg{background:#e7f3ff;padding:10px;border-radius:12px;margin-bottom:10px}
.msg.me{background:#1877f2;color:#fff;text-align:left}
input,textarea{width:100%;padding:12px;border:1px solid #ddd;border-radius:10px;margin-bottom:10px;font-size:15px}
button{width:100%;background:#1877f2;color:#fff;border:none;padding:13px;border-radius:10px;font-size:16px;font-weight:700}
.footer{text-align:center;color:#888;padding:20px;font-size:13px}
.nav{display:flex;gap:8px;overflow:auto;padding:10px;background:#fff}
.nav a{white-space:nowrap;background:#f0f2f5;padding:8px 14px;border-radius:20px;text-decoration:none;color:#333;font-weight:700;font-size:13px}
</style>
"""

def header():
    return f"""
    <div class="top"><div class="logo">Noor<span> Digital</span></div>
    <div><a href="/">الرئيسية</a> <a href="/social">Social</a> <a href="/market">Market</a></div></div>
    <div class="nav">
    <a href="/">🏠 الرئيسية</a><a href="/social">💬 NoorSocial</a><a href="/shot">🎬 NoorShot</a><a href="/chat">💚 NoorChat</a><a href="/market">🛒 NoorMarket</a><a href="/book">📢 NoorBook</a>
    </div>
    """

@app.route("/")
def home():
    return render_template_string(BASE_CSS + header() + """
    <div class="hero"><h1>🔥 Noor Digital Group</h1><p>منصة سودانية واحدة تجمع كل شي<br>تواصل - فيديو - دردشة - سوق - اعلانات</p><br><a href="/social" style="background:#fff;color:#1877f2;padding:12px 25px;border-radius:25px;text-decoration:none;font-weight:900">ابدأ الآن مجاناً</a></div>
    <div class="grid">
        <div class="card"><div class="icon">📘</div><h3>NoorBook</h3><p>مدير اعلانات نور - اعلن ووصل لكل السودان</p><a href="/book">افتح NoorBook</a></div>
        <div class="card"><div class="icon">💬</div><h3>NoorSocial</h3><p>تواصل مع اصحابك - انشر - تفاعل</p><a href="/social">افتح Social</a></div>
        <div class="card"><div class="icon">🎬</div><h3>NoorShot</h3><p>فيديوهات قصيرة - ترند - ارباح</p><a href="/shot">افتح Shot</a></div>
        <div class="card"><div class="icon">💚</div><h3>NoorChat</h3><p>دردشة سريعة وآمنة مع اي زول</p><a href="/chat">افتح Chat</a></div>
        <div class="card"><div class="icon">🛒</div><h3>NoorMarket</h3><p>سوق السودان - بيع واشتري</p><a href="/market">افتح Market</a></div>
        <div class="card"><div class="icon">📊</div><h3>لوحة التحكم</h3><p>تابع مشاهداتك وارباحك</p><a href="/dashboard">افتح الداشبورد</a></div>
    </div>
    <div class="footer">Noor Digital Group © 2026 - صنع في السودان 🇸🇩</div>
    """)

@app.route("/social", methods=["GET","POST"])
def social():
    if request.method=="POST":
        POSTS.insert(0, {"user":"انت","text":request.form.get("text",""),"likes":0})
    posts_html="".join([f'<div class="post"><b>👤 {p["user"]}</b><p>{p["text"]}</p><div class="actions"><span>❤️ {p["likes"]} إعجاب</span><span>💬 تعليق</span><span>↗️ مشاركة</span></div></div>' for p in POSTS])
    return render_template_string(BASE_CSS+header()+f"""
    <div class="container"><h2>💬 NoorSocial - تواصل</h2><br>
    <div class="post"><form method="post"><textarea name="text" placeholder="اكتب شي ..."></textarea><button>انشر الآن</button></form></div>
    {posts_html}</div>""")

@app.route("/shot")
def shot():
    v="".join([f'<div class="video"><h3>{x["title"]}</h3><span>{x["user"]} • {x["views"]} مشاهدة</span><br><br><div style="font-size:60px;text-align:center">▶️</div><br><div style="text-align:center">❤️ 🔥 💬 ↗️</div></div>' for x in VIDEOS])
    return render_template_string(BASE_CSS+header()+f'<div class="container"><h2>🎬 NoorShot - فيديو</h2><br>{v}</div>')

@app.route("/chat")
def chat():
    return render_template_string(BASE_CSS+header()+"""
    <div class="container"><h2>💚 NoorChat - دردشة</h2><br>
    <div class="chatbox"><div class="msg">اهلا يوسف كيفك؟ 👋</div><div class="msg me">تمام والله وانت؟</div><div class="msg">شفت NoorShot الجديد؟ رهيب 🔥</div><form><input placeholder="اكتب رسالة..."><button>ارسال</button></form></div></div>""")

@app.route("/market")
def market():
    p="".join([f'<div class="product"><div class="img">{x["img"]}</div><h3>{x["name"]}</h3><div class="price">{x["price"]}</div><br><button>اشتري الآن 🛒</button></div>' for x in PRODUCTS])
    return render_template_string(BASE_CSS+header()+f'<div class="container"><h2>🛒 NoorMarket - سوق</h2><br><div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">{p}</div></div>')

@app.route("/book")
def book():
    return render_template_string(BASE_CSS+header()+"""
    <div class="container"><h2>📢 NoorBook - مدير اعلانات نور</h2><br>
    <div class="post"><h3>🎯 انشئ اعلانك</h3><p>وصل اعلانك لأكثر من 100,000 شخص في السودان</p><br><input placeholder="اسم الاعلان"><input placeholder="ميزانيتك - مثال 50,000"><button>انشئ حملة اعلانية 🚀</button></div>
    <div class="post"><h3>📊 احصائياتك</h3><p>👀 المشاهدات: 12,450<br>🖱️ النقرات: 1,230<br>💰 التكلفة: 25,000 ج</p></div></div>""")

@app.route("/dashboard")
def dashboard():
    return render_template_string(BASE_CSS+header()+"""
    <div class="container"><h2>📊 لوحة التحكم</h2><br>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">
    <div class="post" style="text-align:center"><h1>12K</h1><p>متابع</p></div>
    <div class="post" style="text-align:center"><h1>45K</h1><p>مشاهدة</p></div>
    <div class="post" style="text-align:center"><h1>850</h1><p>اعجاب</p></div>
    <div class="post" style="text-align:center"><h1>120K</h1><p>ارباح - جنيه</p></div>
    </div></div>""")

if __name__=="__main__":
    port=int(os.environ.get("PORT",5000))
    app.run(host="0.0.0.0",port=port)
