from flask import Flask, render_template_string, request
import os
app = Flask(__name__)

POSTS = [
    {"user":"نور","text":"مرحب بيكم في Noor Digital Group 🔥 أكبر منصة سودانية","img":"","likes":124},
    {"user":"يوسف","text":"NoorShot نزل - صور فيديو واربح 🔥","img":"https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=500","likes":89},
    {"user":"سارة","text":"منو جرب NoorMarket ؟ رهيب والله","img":"","likes":56},
]
PRODUCTS = [
    {"name":"تلفون سامسونج","price":"450,000 ج","img":"📱"},
    {"name":"لابتوب HP","price":"1,200,000 ج","img":"💻"},
    {"name":"سماعة بلوتوث","price":"85,000 ج","img":"🎧"},
    {"name":"ساعة ذكية","price":"120,000 ج","img":"⌚"},
]
VIDEOS = [
    {"title":"فيديو ترند سوداني 🔥","user":"@yousuf","views":"12K","img":"https://images.unsplash.com/photo-1492691527719-9d1e07e534b4?w=500"},
    {"title":"تحدي الضحك 😂","user":"@sara","views":"8K","img":"https://images.unsplash.com/photo-1517841905240-472988babdf9?w=500"},
    {"title":"أغنية جديدة","user":"@noor","views":"25K","img":"https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=500"},
]

CSS = """
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:'Segoe UI',Tahoma,sans-serif}
body{background:#f0f2f5;direction:rtl}
.top{background:#fff;padding:12px 15px;display:flex;justify-content:space-between;align-items:center;box-shadow:0 2px 10px #0001;position:sticky;top:0;z-index:99}
.logo{font-size:22px;font-weight:900;color:#1877f2}.logo span{color:#ff6b00}
.top a{color:#333;text-decoration:none;font-weight:700;margin:0 5px;font-size:14px}
.hero{background:linear-gradient(135deg,#1877f2,#7b2ff7,#ff6b00);color:#fff;padding:35px 20px;text-align:center}
.hero h1{font-size:28px;margin-bottom:10px}.hero p{opacity:.9;line-height:1.6}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;padding:15px}
.card{background:#fff;border-radius:16px;padding:18px;text-align:center;box-shadow:0 2px 10px #0001}
.card .icon{font-size:38px}.card h3{margin:5px 0}.card p{color:#777;font-size:13px;margin-bottom:12px}
.card a{display:block;background:#1877f2;color:#fff;padding:10px;border-radius:10px;text-decoration:none;font-weight:700}
.card:nth-child(2) a{background:#ff6b00}.card:nth-child(3) a{background:#e1306c}.card:nth-child(4) a{background:#00c853}.card:nth-child(5) a{background:#7b2ff7}.card:nth-child(6) a{background:#111}
.container{max-width:600px;margin:auto;padding:15px}
.post{background:#fff;border-radius:14px;padding:15px;margin-bottom:12px;box-shadow:0 1px 5px #0001}
.post img{width:100%;border-radius:12px;margin-top:10px}
.post b{font-size:16px}.post p{margin:10px 0;line-height:1.6}
.actions{display:flex;gap:10px;color:#555;font-size:14px;border-top:1px solid #eee;padding-top:10px}
.product{background:#fff;border-radius:14px;padding:15px;text-align:center}.product .img{font-size:50px}.product .price{color:#00c853;font-weight:900;font-size:18px}
.video{background:#111;color:#fff;border-radius:14px;padding:0;overflow:hidden;margin-bottom:12px}.video img{width:100%;height:220px;object-fit:cover}.video .info{padding:15px}
.nav{display:flex;gap:8px;overflow:auto;padding:10px;background:#fff}.nav a{white-space:nowrap;background:#f0f2f5;padding:8px 14px;border-radius:20px;text-decoration:none;color:#333;font-weight:700;font-size:13px}
input,textarea{width:100%;padding:12px;border:1px solid #ddd;border-radius:10px;margin-bottom:10px;font-size:15px}
button{width:100%;background:#1877f2;color:#fff;border:none;padding:13px;border-radius:10px;font-size:16px;font-weight:700;cursor:pointer}
.upload-row{display:flex;gap:8px;margin-bottom:10px}.upload-row label{flex:1;background:#f0f2f5;text-align:center;padding:10px;border-radius:10px;font-weight:700;font-size:14px;cursor:pointer}
.upload-row input{display:none}
.footer{text-align:center;color:#888;padding:20px;font-size:13px}
</style>
"""
def header():
    return """<div class="top"><div class="logo">Noor<span> Digital</span></div><div><a href="/">الرئيسية</a> <a href="/social">Social</a> <a href="/market">Market</a></div></div>
    <div class="nav"><a href="/">🏠 الرئيسية</a><a href="/social">💬 NoorSocial</a><a href="/shot">🎬 NoorShot</a><a href="/chat">💚 NoorChat</a><a href="/market">🛒 NoorMarket</a><a href="/book">📢 NoorBook</a></div>"""

@app.route("/")
def home():
    return render_template_string(CSS+header()+"""
    <div class="hero"><h1>🔥 Noor Digital Group</h1><p>منصة سودانية واحدة تجمع كل شي<br>تواصل - فيديو - دردشة - سوق - اعلانات</p><br><a href="/social" style="background:#fff;color:#1877f2;padding:12px 25px;border-radius:25px;text-decoration:none;font-weight:900">ابدأ الآن مجاناً</a></div>
    <div class="grid">
    <div class="card"><div class="icon">📘</div><h3>NoorBook</h3><p>مدير اعلانات نور</p><a href="/book">افتح NoorBook</a></div>
    <div class="card"><div class="icon">💬</div><h3>NoorSocial</h3><p>تواصل مع اصحابك</p><a href="/social">افتح Social</a></div>
    <div class="card"><div class="icon">🎬</div><h3>NoorShot</h3><p>فيديوهات قصيرة - ريلز</p><a href="/shot">افتح Shot</a></div>
    <div class="card"><div class="icon">💚</div><h3>NoorChat</h3><p>دردشة سريعة</p><a href="/chat">افتح Chat</a></div>
    <div class="card"><div class="icon">🛒</div><h3>NoorMarket</h3><p>سوق السودان</p><a href="/market">افتح Market</a></div>
    <div class="card"><div class="icon">📊</div><h3>لوحة التحكم</h3><p>تابع ارباحك</p><a href="/dashboard">افتح الداشبورد</a></div>
    </div><div class="footer">Noor Digital Group © 2026 - صنع في السودان 🇸🇩</div>""")

@app.route("/social", methods=["GET","POST"])
def social():
    if request.method=="POST":
        img=request.form.get("img","")
        POSTS.insert(0, {"user":"انت","text":request.form.get("text",""),"img":img,"likes":0})
    posts=""
    for p in POSTS:
        img_tag=f'<img src="{p["img"]}">' if p["img"] else ""
        posts+=f'<div class="post"><b>👤 {p["user"]}</b><p>{p["text"]}</p>{img_tag}<div class="actions"><span>❤️ {p["likes"]} إعجاب</span><span>💬 تعليق</span><span>↗️ مشاركة</span></div></div>'
    return render_template_string(CSS+header()+f"""
    <div class="container"><h2>💬 NoorSocial - تواصل</h2><br>
    <div class="post"><form method="post">
    <textarea name="text" placeholder="اكتب شي ..."></textarea>
    <input name="img" placeholder="🔗 الصق رابط صورة / فيديو هنا (اختياري)">
    <div class="upload-row">
    <label>📷 صورة <input type="file" accept="image/*" onchange="preview(this)"></label>
    <label>🎬 فيديو / ريلز <input type="file" accept="video/*" onchange="alert('تم اختيار الفيديو ✅ - ارفعو وسيظهر قريبا')"></label>
    <label>😀 صورة جاهزة <input type="button" onclick="document.querySelector('[name=img]').value='https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=500';alert('تم اضافة صورة تجريبية ✅ دوس انشر الآن')"></label>
    </div>
    <img id="prev" style="display:none;width:100%;border-radius:12px;margin-bottom:10px">
    <button>انشر الآن 🚀</button></form></div>
    <script>function preview(e){{let r=new FileReader();r.onload=function(){{document.getElementById('prev
