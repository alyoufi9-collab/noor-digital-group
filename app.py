# ==========================================
# Noor Digital Group - المشروع الكل - كود واحد
# انسخ الكود ده كلو والصقو في app.py
# ==========================================
from flask import Flask, render_template_string, request, redirect, session
import os, sqlite3, base64
app = Flask(__name__)
app.secret_key = "noor-2026-full-project"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# ---------- قاعدة البيانات ----------
def db():
    c = sqlite3.connect("noor.db")
    c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, phone TEXT, password TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY, user TEXT, text TEXT, img TEXT, is_video INTEGER, likes INTEGER DEFAULT 0)")
    c.execute("CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, name TEXT, price TEXT, img TEXT)")
    if c.execute("SELECT count(*) FROM products").fetchone()[0] == 0:
        for n,p,i in [("تلفون سامسونج","450,000 ج","📱"),("لابتوب HP","1,200,000 ج","💻"),("سماعة بلوتوث","85,000 ج","🎧"),("ساعة ذكية","120,000 ج","⌚"),("كاميرا","900,000 ج","📷"),("بلايستيشن","1,500,000 ج","🎮")]:
            c.execute("INSERT INTO products (name,price,img) VALUES (?,?,?)",(n,p,i))
    if c.execute("SELECT count(*) FROM posts").fetchone()[0] == 0:
        c.execute("INSERT INTO posts (user,text,img,is_video,likes) VALUES (?,?,?,?,?)",("نور","مرحب بيكم في Noor Digital Group 🔥 اكبر منصة سودانية","",0,124))
        c.execute("INSERT INTO posts (user,text,img,is_video,likes) VALUES (?,?,?,?,?)",("يوسف","NoorShot نزل - صور فيديو واربح 🔥","https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=500",0,89))
        c.execute("INSERT INTO posts (user,text,img,is_video,likes) VALUES (?,?,?,?,?)",("سارة","منو جرب NoorMarket ؟ رهيب والله","",0,56))
    c.commit()
    return c

# ---------- التصميم ----------
CSS = "<style>*{margin:0;padding:0;box-sizing:border-box;font-family:Tahoma}body{background:#f0f2f5;direction:rtl}.top{background:#fff;padding:12px 15px;display:flex;justify-content:space-between;align-items:center;position:sticky;top:0;z-index:99}.logo{font-size:22px;font-weight:900;color:#1877f2}.logo span{color:#ff6b00}.top a{color:#333;text-decoration:none;font-weight:700;margin:0 5px;font-size:13px}.hero{background:linear-gradient(135deg,#1877f2,#7b2ff7,#ff6b00);color:#fff;padding:35px 20px;text-align:center}.hero h1{font-size:28px;margin-bottom:10px}.grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;padding:15px}.card{background:#fff;border-radius:16px;padding:18px;text-align:center;box-shadow:0 2px 10px #0001}.card .icon{font-size:38px}.card p{color:#777;font-size:13px;margin-bottom:12px}.card a{display:block;background:#1877f2;color:#fff;padding:10px;border-radius:10px;text-decoration:none;font-weight:700}.card:nth-child(2) a{background:#ff6b00}.card:nth-child(3) a{background:#e1306c}.card:nth-child(4) a{background:#00c853}.card:nth-child(5) a{background:#7b2ff7}.card:nth-child(6) a{background:#111}.container{max-width:600px;margin:auto;padding:15px}.post{background:#fff;border-radius:14px;padding:15px;margin-bottom:12px;box-shadow:0 1px 5px #0001}.post img,.post video{width:100%;border-radius:12px;margin-top:10px}.actions{display:flex;gap:10px;color:#555;font-size:14px;border-top:1px solid #eee;padding-top:10px}.product{background:#fff;border-radius:14px;padding:15px;text-align:center;box-shadow:0 1px 5px #0001}.product .price{color:#00c853;font-weight:900}.nav{display:flex;gap:8px;overflow:auto;padding:10px;background:#fff}.nav a{white-space:nowrap;background:#f0f2f5;padding:8px 14px;border-radius:20px;text-decoration:none;color:#333;font-weight:700;font-size:13px}input,textarea{width:100%;padding:12px;border:1px solid #ddd;border-radius:10px;margin-bottom:10px;font-size:15px}button{width:100%;background:#1877f2;color:#fff;border:none;padding:13px;border-radius:10px;font-size:16px;font-weight:700;cursor:pointer}.upload-row{display:flex;gap:8px;margin-bottom:10px}.upload-row label{flex:1;background:#f0f2f5;text-align:center;padding:10px;border-radius:10px;font-weight:700;font-size:14px}.upload-row input{display:none}.footer{text-align:center;color:#888;padding:20px}</style>"

def header():
    u = session.get("user","زائر")
    return '<div class="top"><div class="logo">Noor<span> Digital</span></div><div><span>👤 '+u+'</span> <a href="/login">دخول</a> <a href="/logout">خروج</a></div></div><div class="nav"><a href="/">🏠 الرئيسية</a><a href="/social">💬 Social</a><a href="/shot">🎬 Shot</a><a href="/chat">💚 Chat</a><a href="/market">🛒 Market</a><a href="/book">📢 Book</a><a href="/dashboard">📊 داشبورد</a></div>'

# ---------- 1 - الرئيسية ----------
@app.route("/")
def home():
    return render_template_string(CSS+header()+'<div class="hero"><h1>🔥 Noor Digital Group</h1><p>المشروع الكل في محل واحد<br>تواصل - فيديو - دردشة - سوق - اعلانات<br>مرحب بيك يا '+session.get("user","ضيف")+'</p><br><a href="/social" style="background:#fff;color:#1877f2;padding:12px 25px;border-radius:25px;text-decoration:none;font-weight:900">ابدأ الآن مجانا</a></div><div class="grid"><div class="card"><div class="icon">📘</div><h3>NoorBook</h3><p>مدير اعلانات نور - وصل لكل السودان</p><a href="/book">افتح NoorBook</a></div><div class="card"><div class="icon">💬</div><h3>NoorSocial</h3><p>تواصل - انشر صورة وفيديو</p><a href="/social">افتح Social</a></div><div class="card"><div class="icon">🎬</div><h3>NoorShot</h3><p>فيديوهات قصيرة - ريلز - ارباح</p><a href="/shot">افتح Shot</a></div><div class="card"><div class="icon">💚</div><h3>NoorChat</h3><p>دردشة سريعة وآمنة</p><a href="/chat">افتح Chat</a></div><div class="card"><div class="icon">🛒</div><h3>NoorMarket</h3><p>سوق السودان - بيع واشتري</p><a href="/market">افتح Market</a></div><div class="card"><div class="icon">📊</div><h3>لوحة التحكم</h3><p>تابع مشاهداتك وارباحك</p><a href="/dashboard">افتح الداشبورد</a></div></div><div class="footer">Noor Digital Group © 2026 - صنع في السودان 🇸🇩 - المشروع الكل</div>')

# ---------- 2 - دخول / حساب ----------
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method=="POST":
        name=request.form.get("name"); pw=request.form.get("password")
        c=db(); r=c.execute("SELECT * FROM users WHERE name=? AND password=?",(name,pw)).fetchone()
        if r:
            session["user"]=name; return redirect("/")
        else:
            c.execute("INSERT INTO users (name,phone,password) VALUES (?,?,?)",(name,"",pw)); c.commit(); session["user"]=name; return redirect("/")
    return render_template_string(CSS+header()+'<div class="container"><h2>🔐 دخول / انشاء حساب</h2><br><div class="post"><form method="post"><input name="name" placeholder="اسمك - مثلا يوسف" required><input name="password" type="password" placeholder="كلمة السر" required><button>دخول / انشاء حساب 🚀</button></form><p style="text-align:center;color:#888;font-size:13px;margin-top:10px">لو ما عندك حساب - حيتعمل ليك طوالي</p></div></div>')
@app.route("/logout")
def logout():
    session.pop("user",None); return redirect("/")

# ---------- 3 - NoorSocial ----------
@app.route("/social", methods=["GET","POST"])
def social():
    c=db()
    if request.method=="POST":
        txt=request.form.get("text",""); link=request.form.get("img",""); img=link; is_video=0
        f=request.files.get("file")
        if f and f.filename!="":
            data=f.read(); b64=base64.b64encode(data).decode()
            img="data:"+f.content_type+";base64,"+b64
            is_video=1 if "video" in f.content_type else 0
        user=session.get("user","انت")
        c.execute("INSERT INTO posts (user,text,img,is_video) VALUES (?,?,?,?)",(user,txt,img,is_video)); c.commit()
        return redirect("/social")
    rows=c.execute("SELECT * FROM posts ORDER BY id DESC").fetchall()
    posts=""
    for r in rows:
        media=""
        if r[3]:
            if r[4]: media='<video src="'+r[3]+'" controls></video>'
            else: media='<img src="'+r[3]+'">'
        posts+='<div class="post"><b>👤 '+r[1]+'</b><p>'+r[2]+'</p>'+media+'<div class="actions"><span>❤️ '+str(r[5])+' اعجاب</span><span>💬 تعليق</span><span>↗️ مشاركة</span></div></div>'
    form='<div class="container"><h2>💬 NoorSocial - تواصل</h2><br><div class="post"><form method="post" enctype="multipart/form-data"><textarea name="text" placeholder="اكتب شي ..."></textarea><input name="img" placeholder="او الصق رابط صورة هنا"><div class="upload-row"><label>📷 صورة / 🎬 فيديو قصير<input type="file" name="file" accept="image/*,video/*" onchange="previewFile(this)"></label></div><img id="prev" style="display:none;width:100%;border-radius:12px;margin-bottom:10px"><video id="prevV" controls style="display:none;width:100%;border-radius:12px;margin-bottom:10px"></video><p style="color:#888;font-size:12px;text-align:center">الفيديو لازم يكون قصير - اقل من 10 ميقا</p><button>انشر الآن 🚀</button></form></div>'
    js="<script>function previewFile(e){var f=e.files[0];if(!f)return;if(f.size>10000000){alert('الفيديو كبير - اختار فيديو اقل من 10 ميقا');e.value='';return;}var r=new FileReader();r.onload=function(){if(f.type.includes('video')){document.getElementById('prevV').src=r.result;document.getElementById('prevV').style.display='block';document.getElementById('prev').style.display='none';}else{document.getElementById('prev').src=r.result;document.getElementById('prev').style.display='block';document.getElementById('prevV').style.display='none';}};r.readAsDataURL(f);}</script>"
    return render_template_string(CSS+header()+form+posts+"</div>"+js)

# ---------- 4 - NoorShot ----------
@app.route("/shot")
def shot():
    c=db(); rows=c.execute("SELECT * FROM posts ORDER BY id DESC").fetchall()
    v=""
    for r in rows:
        if r[4]: v+='<div class="post"><b>👤 '+r[1]+'</b><p>'+r[2]+'</p><video src="'+r[3]+'" controls></video><div class="actions"><span>❤️ '+str(r[5])+'</span><span>💬 تعليق</span><span>↗️ مشاركة</span></div></div>'
        elif r[3]: v+='<div class="post"><b>👤 '+r[1]+'</b><p>'+r[2]+'</p><img src="'+r[3]+'"><div class="actions"><span>❤️ '+str(r[5])+'</span><span>💬 تعليق</span><span>↗️ مشاركة</span></div></div>'
    if not v: v='<div class="post"><p>لسه ما في ريلز - انشر اول ريلز من Social</p></div>'
    return render_template_string(CSS+header()+'<div class="container"><h2>🎬 NoorShot - ريلز</h2><br><div style="background:#fff;padding:15px;border-radius:14px;margin-bottom:12px;text-align:center"><a href="/social" style="background:#e1306c;color:#fff;padding:12px 20px;border-radius:25px;font-weight:700;text-decoration:none;display:block">🎬 + انشر ريلز جديد</a></div>'+v+'</div>')

# ---------- 5 - NoorChat ----------
@app.route("/chat")
def chat():
    return render_template_string(CSS+header()+'<div class="container"><h2>💚 NoorChat - دردشة</h2><br><div class="post"><p>اهلا '+session.get("user","ضيف")+' كيفك؟ 👋</p></div><div class="post" style="background:#1877f2;color:#fff"><p>تمام والله وانت؟</p></div><div class="post"><p>شفت NoorShot الجديد؟ رهيب 🔥</p></div><form onsubmit="alert(\'تم الارسال ✅\');return false"><input placeholder="اكتب رسالة..."><button>ارسال 💬</button></form></div>')

# ---------- 6 - NoorMarket ----------
@app.route("/market")
def market():
    c=db(); rows=c.execute("SELECT * FROM products").fetchall()
    p=""
    for r in rows: p+='<div class="product"><div style="font-size:50px">'+r[3]+'</div><h3>'+r[1]+'</h3><div class="price">'+r[2]+'</div><br><a href="/order/'+str(r[0])+'" style="background:#00c853;color:#fff;padding:10px;border-radius:10px;text-decoration:none;display:block">اشتري الآن 🛒</a></div>'
    return render_template_string(CSS+header()+'<div class="container"><h2>🛒 NoorMarket - سوق السودان</h2><br><div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">'+p+'</div></div>')
@app.route("/order/<int:pid>")
def order(pid):
    c=db(); r=c.execute("SELECT * FROM products WHERE id=?",(pid,)).fetchone()
    return render_template_string(CSS+header()+f'<div class="container"><h2>✅ تم الطلب بنجاح</h2><br><div class="post" style="text-align:center"><div style="font-size:60px">{r[3]}</div><h2>{r[1]}</h2><p>السعر: {r[2]}</p><p>شكرا يا {session.get("user","ضيف")} - طلبك وصل ✅<br>حنتواصل معاك قريب</p><a href="/market" style="background:#1877f2;color:#fff;padding:12px;border-radius:10px;text-decoration:none;display:block">رجوع للسوق</a></div></div>')

# ---------- 7 - NoorBook ----------
@app.route("/book")
def book():
    return render_template_string(CSS+header()+'<div class="container"><h2>📢 NoorBook - مدير اعلانات نور</h2><br><div class="post"><h3>🎯 انشئ اعلانك</h3><p>وصل اعلانك لأكثر من 100,000 شخص في السودان</p><br><form onsubmit="alert(\'تم انشاء حملتك ✅\');return false"><input placeholder="اسم الاعلان"><input placeholder="ميزانيتك - مثال 50,000"><input placeholder="رابط صورة الاعلان"><button>انشئ حملة اعلانية 🚀</button></form></div><div class="post"><h3>📊 احصائياتك</h3><p>👀 المشاهدات: 12,450<br>🖱️ النقرات: 1,230<br>💰 التكلفة: 25,000 ج</p></div></div>')

# ---------- 8 - Dashboard ----------
@app.route("/dashboard")
def dash():
    c=db(); cnt=c.execute("SELECT count(*) FROM posts").fetchone()[0]; users=c.execute("SELECT count(*) FROM users").fetchone()[0]
    return render_template_string(CSS+header()+f'<div class="container"><h2>📊 لوحة التحكم - المشروع الكل</h2><br><div style="display:grid;grid-template-columns:1fr 1fr;gap:12px"><div class="post" style="text-align:center"><h1>{users}</h1><p>مستخدم مسجل</p></div><div class="post" style="text-align:center"><h1>{cnt}</h1><p>منشور محفوظ</p></div><div class="post" style="text-align:center"><h1>45K</h1><p>مشاهدة</p></div><div class="post" style="text-align:center"><h1>120K</h1><p>ارباح - جنيه</p></div></div></div>')

# ---------- تشغيل ----------
if __name__=="__main__":
    port=int(os.environ.get("PORT",5000))
    app.run(host="0.0.0.0",port=port)
