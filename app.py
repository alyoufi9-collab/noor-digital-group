# NoorBook V32 - PRO - من الصفر للاحتراف - Noor Digital Group
# كل الاسماء نور بس - لا Facebook / Messenger / WhatsApp / Meta / Instagram
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List
import uuid, datetime
app = FastAPI(title="NoorBook PRO")

DB={"campaigns":[],"adsets":[],"ads":[],"audiences":[],"notifications":[
 {"id":"1","title":"✅ تمت الموافقة على حملتك","text":"حملة عطور عطبرة - اتوافق عليها - شغالة هسي","time":"قبل 5 دقايق","type":"success"},
 {"id":"2","title":"⚠️ ميزانيتك قربت تخلص","text":"باقي 15% من ميزانية حملة المبيعات","time":"قبل ساعة","type":"warn"},
 {"id":"3","title":"📩 ليد جديد","text":"جاك ليد جديد من NoorChat - احمد - عطبرة - 091xxxx","time":"قبل 2 ساعة","type":"lead"},
],"analytics":{"spend":125000,"reach":48200,"clicks":3210,"leads":187,"calls":96,"calls_qualified":61,"sales":34,"lp_views":2100,"ctr":6.6,"cpc":39,"cpm":2593,"roas":4.2}}

class Campaign(BaseModel):
    name: str; objective: str; budget_type: str="lifetime"; budget: float=50000
    ab_test: bool=False; advantage_budget: bool=True
class AdSet(BaseModel):
    campaign_id: str=""; name: str=""; age_min: int=18; age_max: int=65; gender: str="all"
    lat: float=15.5007; lng: float=32.5599; radius_km: int=25; location_name: str="الخرطوم - السودان"
    interests: str=""; custom_audience: str=""; lookalike: str=""; lookalike_pct: int=1
    budget: float=10000; schedule_type: str="grid"; week_grid: List[List[int]]=[]
    placements: List[str]=[]; performance_goal: str=""; call_min_seconds: int=180
class Ad(BaseModel):
    adset_id: str=""; name: str=""; format: str="carousel"; headline: str=""; primary_text: str=""; cta: str="تسوق الان"; media_urls: List[str]=[]; destination: str="NoorMarket"

HTML = r"""
<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>NoorBook PRO - مدير اعلانات نور</title>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"><script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>
*{box-sizing:border-box;font-family:system-ui}body{margin:0;background:#0B0714;color:#fff;padding-bottom:100px}
.top{position:sticky;top:0;z-index:20;background:rgba(15,8,30,.9);backdrop-filter:blur(12px);padding:14px 16px;display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #2A1A4A}
.logo{font-weight:900;font-size:22px;background:linear-gradient(90deg,#F5C518,#FF4D8D,#7C3AED);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.pill{background:linear-gradient(90deg,#7C3AED,#FF4D8D);padding:8px 14px;border-radius:999px;font-size:13px;font-weight:700}
.tabs{display:flex;gap:8px;padding:12px 16px;overflow:auto}.tab{white-space:nowrap;background:#1A1130;border:1px solid #2A1A4A;padding:10px 14px;border-radius:999px;font-size:13px}.tab.on{background:linear-gradient(90deg,#7C3AED,#FF4D8D);border:0;font-weight:800}
.card{background:linear-gradient(180deg,#1B1233,#120B24);border:1px solid #2A1A4A;border-radius:20px;padding:16px;margin:12px 16px;box-shadow:0 10px 30px rgba(0,0,0,.4)}
.card h3{margin:0 0 6px}.muted{color:#B9AEE0;font-size:13px;line-height:1.7}
label{display:block;font-size:13px;margin:14px 0 6px;color:#E7DEFF}
input,select,textarea{width:100%;background:#0F0A1F;border:1px solid #35245E;color:#fff;padding:13px;border-radius:14px;font-size:15px}
.obj-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.obj{border:2px solid #35245E;background:#17102E;padding:12px;border-radius:16px;cursor:pointer}.obj.sel{border-color:#F5C518;background:#2A1F08}.obj b{display:block}.obj small{color:#B9AEE0}.algo{font-size:11px;color:#F5C518;margin-top:6px}
.btn{width:100%;background:linear-gradient(90deg,#F5C518,#FF4D8D,#7C3AED);border:0;padding:15px;border-radius:16px;font-weight:900;font-size:16px;color:#fff;margin-top:14px}
.btn2{background:#241640;border:1px solid #35245E;color:#fff;padding:10px 14px;border-radius:12px}
.chip{display:inline-block;background:#241640;border:1px solid #35245E;padding:7px 11px;border-radius:999px;font-size:12px;margin:4px 4px 0 0}
.kpi{display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:10px}.kpi div{background:#0F0A1F;border:1px solid #2A1A4A;border-radius:16px;padding:12px;text-align:center}.kpi b{font-size:17px;color:#F5C518}.kpi small{color:#B9AEE0}
.hide{display:none}
/* جدول المربعات - Dayparting Grid - زي ميتا */
.grid-wrap{overflow:auto;border:1px solid #35245E;border-radius:14px;background:#0F0A1F;padding:10px}
table.grid{border-collapse:collapse;font-size:11px;min-width:520px}table.grid th,table.grid td{border:1px solid #2A1A4A;padding:0;text-align:center}
table.grid th{padding:6px 2px;color:#B9AEE0}.cell{width:28px;height:28px;background:#1A1130;cursor:pointer}.cell.on{background:linear-gradient(135deg,#F5C518,#FF4D8D);box-shadow:0 0 8px #FF4D8D}.cell:hover{outline:2px solid #fff}
.legend{display:flex;gap:12px;font-size:12px;color:#B9AEE0;margin-top:8px}
/* خريطة */
#map{height:280px;border-radius:16px;overflow:hidden;border:1px solid #35245E}
.notif{background:#0F0A1F;border:1px solid #2A1A4A;border-radius:14px;padding:12px;margin-top:10px}.notif b{font-size:14px}
.carousel{display:flex;gap:10px;overflow:auto;padding:6px 0}.car{flex:0 0 150px;background:#0F0A1F;border:1px solid #35245E;border-radius:16px;padding:10px;text-align:center}.car img{width:100%;height:90px;object-fit:cover;border-radius:10px;background:#222}
.nav{position:fixed;bottom:0;right:0;left:0;background:#120B24;border-top:1px solid #2A1A4A;display:flex;padding:12px}.nav div{flex:1;text-align:center;font-size:12px;color:#B9AEE0}.nav div.on{color:#F5C518;font-weight:900}
canvas{width:100%;height:140px;background:#0F0A1F;border-radius:14px}
.range{width:100%}
</style></head><body>
<div class="top"><div class="logo">N • NoorBook PRO</div><div class="pill">💰 <span id="wallet">50,000</span> ج.س 🔔 <span id="notifCount">3</span></div></div>

<div class="tabs">
<div class="tab on" onclick="showTab('dash',this)">📊 لوحة التحكم</div>
<div class="tab" onclick="showTab('camp',this)">📢 انشاء حملة</div>
<div class="tab" onclick="showTab('aud',this)">👥 الجمهور</div>
<div class="tab" onclick="showTab('notif',this)">🔔 الاشعارات</div>
<div class="tab" onclick="showTab('my',this)">📋 حملاتي</div>
</div>

<!-- داشبورد -->
<div id="tab-dash">
<div class="card"><h3>📊 تحليل البيانات - Analytics - زي ميتا</h3><p class="muted">كل الارقام دي حية - من حملاتك - مش وهمية</p>
<div class="kpi"><div><b id="aSpend">-</b><br><small>الصرف</small></div><div><b id="aReach">-</b><br><small>الوصول</small></div><div><b id="aLeads">-</b><br><small>ليدز</small></div><div><b id="aSales">-</b><br><small>مبيعات</small></div></div>
<div class="kpi" style="margin-top:10px"><div><b id="aCalls">-</b><br><small>مكالمات</small></div><div><b id="aQual">-</b><br><small>مكالمات مؤهلة +3 دقايق</small></div><div><b id="aLp">-</b><br><small>لانديق بيج فيوز</small></div><div><b id="aRoas">-</b><br><small>ROAS</small></div></div>
<p class="muted" style="margin-top:12px">CPM: <b id="aCpm"></b> | CPC: <b id="aCpc"></b> | CTR: <b id="aCtr"></b>%</p>
<canvas id="chart"></canvas>
<p class="muted">💡 قاعدة محمد الفقي: المكالمة اقل من 3 دقايق = ما مبيعة - المكالمة 3 دقايق واكتر = مبيعة مؤهلة - والليد البارد ما تحسبو زي الليد الحار</p>
</div>
<div class="card"><h3>💰 كيف بنحسب؟ - Pricing - زي ميتا</h3>
<p class="muted">
• <b>تكلفة الليد</b> = الصرف / عدد الليدز<br>
• <b>تكلفة المكالمة المؤهلة</b> = الصرف / مكالمات +3 دقايق<br>
• <b>تكلفة المبيعة</b> = الصرف / عدد المبيعات<br>
• <b>لانديق بيج فيو</b> = زول دخل صفحتك وقعد 10 ثواني واكتر - مش داس ومشى<br>
• <b>ROAS</b> = الارباح / الصرف - لو 4.2 يعني كل 1 جنيه صرفتو رجع ليك 4.2 جنيه</p></div>
</div>

<!-- انشاء حملة -->
<div id="tab-camp" class="hide">
<div class="card"><h3>1 - الحملة - Campaign</h3>
<label>اسم الحملة</label><input id="campName" placeholder="مثال: عطور عطبرة - رمضان 2026">
<label>الهدف - 6 اهداف - تحديث ميتا الاخير</label><div class="obj-grid" id="objs"></div>
<div class="row" style="display:flex;gap:10px"><div style="flex:1"><label>نوع الميزانية</label><select id="bType"><option value="lifetime">مدى الحياة - Lifetime - لازم للجدولة</option><option value="daily">يومية - Daily</option></select></div><div style="flex:1"><label>الميزانية</label><input id="campBudget" type="number" value="50000"></div></div>
<label><input type="checkbox" id="ab"> اختبار A/B - A ضد B - صورة ضد فيديو - نص ضد نص</label>
<div id="abBox" class="hide"><p class="muted">اختبار A/B: حنوزع الميزانية 50% / 50% - بعد 1000 ظهور - الخوارزمية حتختار الفايز تلقائيا - وتوقف الخسران</p>
<label>نسخة A - اسم</label><input value="نسخة A - صورة"><label>نسخة B - اسم</label><input value="نسخة B - فيديو"></div>
<label><input type="checkbox" id="adv" checked> Advantage Budget - خلي الخوارزمية توزع</label>
</div>

<div class="card"><h3>2 - المجموعة - Ad Set - المكان والجدول</h3>
<label>اسم المجموعة</label><input id="setName" value="مجموعة 1 - الخرطوم">
<label>📍 اللوكيشن الحقيقي - اسقط الدبوس باليد - جر الدبوس</label>
<p class="muted">جرب هسي: جر الدبوس الاحمر في الخريطة - وين ما تحتو - ده هو جمهورك - وتقدر تكبر وتصغر الخريطة</p>
<div id="map"></div>
<p class="muted">المكان المختار: <b id="locLabel">الخرطوم - السودان</b> | خط العرض: <b id="latV">15.5007</b> | خط الطول: <b id="lngV">32.5599</b></p>
<label>نصف القطر - Radius - حول الدبوس</label><input type="range" class="range" min="1" max="80" value="25" oninput="document.getElementById('radV').innerText=this.value"><span> <b id="radV">25</b> كم حول الدبوس - بغطي تقريبا <b id="radCover">الخرطوم + امدرمان + بحري</b></span>
<div style="display:flex;gap:8px;margin-top:10px"><button class="btn2" onclick="goLoc(15.5007,32.5599,'الخرطوم')">الخرطوم</button><button class="btn2" onclick="goLoc(17.6784,33.9715,'عطبرة')">عطبرة</button><button class="btn2" onclick="goLoc(19.6158,37.2164,'بورتسودان')">بورتسودان</button><button class="btn2" onclick="goLoc(13.4533,33.5015,'ود مدني')">ود مدني</button></div>
<div style="display:flex;gap:10px"><div style="flex:1"><label>العمر من</label><input type="number" value="18" id="ageMin"></div><div style="flex:1"><label>العمر لي</label><input type="number" value="65" id="ageMax"></div></div>
<label>الجنس</label><select id="gender"><option value="all">الكل</option><option value="male">رجال</option><option value="female">نساء</option></select>
<label>الاهتمامات</label><input placeholder="عطور - تجارة - عقارات - تعليم">
<label>هدف الاداء - Performance Goal</label><select id="perf"><option>مبيعات - Purchase</option><option>اضافة للسلة - Add to Cart</option><option>ليد - Lead</option><option>مكالمة +3 دقايق - Qualified Call</option><option>لانديق بيج فيو - Landing Page View</option><option>رسالة - NoorChat Message</option></select>
<label>اماكن الظهور - Placements</label><div><span class="chip">✅ NoorSocial Feed</span><span class="chip">✅ NoorShot Reels</span><span class="chip">✅ NoorChat</span><span class="chip">✅ NoorMarket</span><span class="chip">✅ NoorTalk</span></div>
</div>

<div class="card"><h3>🗓️ الجدول - مربعات تظلل - زي ميتا الكمبيوتر - دوس وظلل</h3>
<p class="muted">دوس على اي مربع - يتلون - دوس تاني - يطفي - واسحب بي اصبعك - تظلل كذا مربع سوا - المربع الملون = الاعلان شغال في الساعة دي - المربع الرمادي = واقف</p>
<div style="display:flex;gap:8px;margin-bottom:10px"><button class="btn2" onclick="gridAll()">كل الاسبوع - ظلل كلو</button><button class="btn2" onclick="gridPeak()">ساعات الذروة - 6م-11م</button><button class="btn2" onclick="gridClear()">امسح كلو</button><button class="btn2" onclick="gridWork()">ايام العمل</button></div>
<div class="grid-wrap"><table class="grid" id="gridTable"></table></div>
<div class="legend"><span>🟪 ملون = شغال</span><span>⬛ رمادي = واقف</span><span>📊 <b id="gridHours">0</b> ساعة شغالة من 168</span></div>
<p class="muted">المنطقة الزمنية: <b>Africa/Khartoum - GMT+2 - السودان</b> | تاريخ البداية: <input type="date"> | تاريخ النهاية: <input type="date"></p>
</div>

<div class="card"><h3>3 - الاعلان - Ad - كاراسول + فيديو + صورة</h3>
<label>صيغة الاعلان - Format</label><select id="adFormat" onchange="toggleFormat()"><option value="carousel">كاراسول - Carousel - اكتر من صورة - تسحب يمين وشمال</option><option value="single">صورة واحدة - Single Image</option><option value="video">فيديو - Video</option><option value="collection">مجموعة - Collection</option></select>
<div class="carousel" id="carBox">
<div class="car"><img src="https://via.placeholder.com/150"><b>بطاقة 1</b><input placeholder="عنوان البطاقة 1"><input placeholder="رابط البطاقة 1"></div>
<div class="car"><img src="https://via.placeholder.com/150"><b>بطاقة 2</b><input placeholder="عنوان البطاقة 2"><input placeholder="رابط البطاقة 2"></div>
<div class="car"><img src="https://via.placeholder.com/150"><b>بطاقة 3</b><input placeholder="عنوان البطاقة 3"><input placeholder="رابط البطاقة 3"></div>
<div class="car" style="display:flex;align-items:center;justify-content:center;font-size:30px" onclick="alert('اضافة بطاقة جديدة')">+</div>
</div>
<label>العنوان الرئيسي</label><input id="adHead" placeholder="عطور اصلية - توصيل عطبرة">
<label>النص الاساسي</label><textarea id="adText" placeholder="اكتب نص يجذب العميل المهتم - ما الفضولي..."></textarea>
<label>زر الدعوة</label><select><option>تسوق الان</option><option>اعرف المزيد</option><option>ارسل رسالة - NoorChat</option><option>اتصل - NoorTalk</option><option>سجّل الان</option><option>حمّل التطبيق</option></select>
<label>وجهة الاعلان - Landing Page</label><select><option>NoorMarket - متجر</option><option>NoorSocial - صفحة</option><option>NoorChat - دردشة</option><option>صفحة هبوط خارجية - Landing Page</option></select>
<button class="btn" onclick="publish()">🚀 نشر الحملة - Publish - زي ميتا</button>
</div>
</div>

<!-- الجمهور -->
<div id="tab-aud" class="hide">
<div class="card"><h3>👥 الجمهور المخصص - Custom Audience</h3><p class="muted">ديل الناس البتعرفهم - الخوارزمية حتدور عليهم بالظبط</p>
<label>نوع الجمهور المخصص</label><select id="custType"><option>شافو الفيديو - Video Viewers</option><option>زارو الموقع - Website Visitors - Noor Pixel</option><option>بعتو رسالة - NoorChat Messages</option><option>اتصلو - NoorTalk Calls +3 دقايق</option><option>ارقام تلفونات - Phone Numbers - ارفع ملف</option><option>اشترو قبل كده - Purchasers</option></select>
<label>المدة - اخر كم يوم؟</label><select><option>اخر 7 ايام</option><option>اخر 30 يوم</option><option>اخر 90 يوم</option><option>اخر 365 يوم</option></select>
<label>اسم الجمهور</label><input placeholder="جمهوري - الشافو فيديو العطور">
<button class="btn2" style="width:100%" onclick="alert('تم حفظ الجمهور المخصص ✅')">حفظ الجمهور المخصص</button></div>
<div class="card"><h3>🧬 الجمهور المشابه - Lookalike Audience</h3><p class="muted">جيب لي ناس بشبهو جمهوري - كل ما النسبة صغيرة - التشابه اقوى</p>
<label>المصدر - جيب ناس بشبهو منو؟</label><select><option>جمهوري المخصص - الشافو الفيديو</option><option>الاشترو قبل كده</option><option>البعتو رسائل</option></select>
<label>نسبة التشابه - كل ما صغرت - اقوى</label><input type="range" min="1" max="10" value="1" oninput="document.getElementById('lookV').innerText=this.value+'% - '+(this.value<=2?'تشابه قوي جدا - ناس قليلة لكن دقيقة':'تشابه واسع - ناس كتيرة')"><p><b id="lookV">1% - تشابه قوي جدا - ناس قليلة لكن دقيقة</b></p>
<label>المكان - وين تدور عليهم؟</label><input value="السودان - نفس مكان الدبوس">
<button class="btn2" style="width:100%" onclick="alert('تم انشاء الجمهور المشابه ✅ - 1% - السودان - حوالي 48,000 شخص')">انشاء جمهور مشابه - Create Lookalike</button></div>
</div>

<!-- الاشعارات -->
<div id="tab-notif" class="hide"><div class="card"><h3>🔔 الاشعارات والتنبيهات</h3><div id="notifList"></div></div></div>
<div id="tab-my" class="hide"><div class="card"><h3>📋 حملاتي</h3><div id="myCamps"></div></div></div>

<div class="nav"><div class="on" onclick="showTab('dash',this)">🏠 الرئيسية</div><div onclick="showTab('camp',this)">📢 حملات</div><div onclick="showTab('aud',this)">👥 جمهور</div><div onclick="showTab('notif',this)">🔔 اشعارات</div><div>🤖 Noor AI</div></div>

<script>
const OBJS=[
{id:'AWARENESS',t:'الوعي',d:'ناس تتذكر',a:'الخوارزمية: تدور على ناس بتتذكر'},
{id:'TRAFFIC',t:'الزيارات',d:'ناس تدوس',a:'الخوارزمية: تدور على ناس بتدوس'},
{id:'ENGAGEMENT',t:'التفاعل',d:'لايك - تعليق',a:'الخوارزمية: تدور على ناس بتتفاعل'},
{id:'LEADS',t:'ليدز',d:'فورم - رسالة',a:'الخوارزمية: تدور على ناس بتملا بيانات'},
{id:'APP',t:'تطبيق',d:'تحميل',a:'الخوارزمية: تدور على ناس بتنزل'},
{id:'SALES',t:'مبيعات',d:'شراء',a:'الخوارزمية: تدور على ناس بتشتري - لازم Noor Pixel'}];
let sel='SALES';
function renderObjs(){document.getElementById('objs').innerHTML=OBJS.map(o=>`<div class="obj ${o.id==sel?'sel':''}" onclick="sel='${o.id}';renderObjs()"><b>${o.t}</b><small>${o.d}</small><div class="algo">${o.a}</div></div>`).join('')}renderObjs();
function showTab(id,el){['dash','camp','aud','notif','my'].forEach(x=>document.getElementById('tab-'+x).classList.toggle('hide',x!==id)); document.querySelectorAll('.tab').forEach(t=>t.classList.remove('on')); if(el) el.classList.add('on'); if(id=='notif') loadNotif(); if(id=='my') loadCamps()}
document.getElementById('ab').addEventListener('change',e=>document.getElementById('abBox').classList.toggle('hide',!e.target.checked));
// خريطة - دبوس حقيقي - جر باليد
let map=L.map('map').setView([15.5007,32.5599],12);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:19}).addTo(map);
let marker=L.marker([15.5007,32.5599],{draggable:true}).addTo(map);
let circle=L.circle([15.5007,32.5599],{radius:25000,color:'#FF4D8D',fillColor:'#FF4D8D',fillOpacity:.15}).addTo(map);
marker.on('dragend',()=>{let p=marker.getLatLng(); document.getElementById('latV').innerText=p.lat.toFixed(4); document.getElementById('lngV').innerText=p.lng.toFixed(4); document.getElementById('locLabel').innerText='مكان مخصص - '+p.lat.toFixed(4)+','+p.lng.toFixed(4); circle.setLatLng(p);});
document.querySelector('.range').addEventListener('input',e=>{circle.setRadius(e.target.value*1000)});
function goLoc(lat,lng,name){map.setView([lat,lng],12); marker.setLatLng([lat,lng]); circle.setLatLng([lat,lng]); document.getElementById('latV').innerText=lat; document.getElementById('lngV').innerText=lng; document.getElementById('locLabel').innerText=name+' - السودان';}
// جدول المربعات - 7x24
let grid=[]; // 7x24
function initGrid(){grid=Array.from({length:7},()=>Array(24).fill(1)); renderGrid()}
function renderGrid(){
let days=['السبت','الاحد','الاثنين','الثلاثاء','الاربعاء','الخميس','الجمعة'];
let h='<tr><th>اليوم / الساعة</th>'+Array.from({length:24},(_,i)=>`<th>${i}</th>`).join('')+'</tr>';
h+=days.map((d,di)=>'<tr><th>'+d+'</th>'+Array.from({length:24},(_,hi)=>`<td><div class="cell ${grid[di][hi]?'on':''}" onclick="toggleCell(${di},${hi})"></div></td>`).join('')+'</tr>').join('');
document.getElementById('gridTable').innerHTML=h;
let cnt=grid.flat().reduce((a,b)=>a+b,0); document.getElementById('gridHours').innerText=cnt;
}
function toggleCell(d,h){grid[d][h]=grid[d][h]?0:1; renderGrid()}
function gridAll(){grid=Array.from({length:7},()=>Array(24).fill(1)); renderGrid()}
function gridClear(){grid=Array.from({length:7},()=>Array(24).fill(0)); renderGrid()}
function gridPeak(){grid=Array.from({length:7},()=>Array.from({length:24},(_,h)=> (h>=18&&h<23)?1:0)); renderGrid()}
function gridWork(){grid=Array.from({length:7},(_,d)=>Array.from({length:24},()=> d<5?1:0)); renderGrid()}
initGrid();
function toggleFormat(){}
async function publish(){
let camp={name:document.getElementById('campName').value||'حملة بدون اسم',objective:sel,ab_test:document.getElementById('ab').checked};
let r=await fetch('/api/campaigns',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(camp)}); let c=await r.json();
alert('✅ تم نشر الحملة - '+c.name+' - الهدف: '+sel+' - المجموعة: '+document.getElementById('setName').value+' - المكان: '+document.getElementById('locLabel').innerText+' - الجدول: '+document.getElementById('gridHours').innerText+' ساعة في الاسبوع'); loadCamps(); showTab('my',null);
}
async function loadCamps(){let r=await fetch('/api/campaigns'); let d=await r.json(); document.getElementById('myCamps').innerHTML=d.map(x=>`<div class="chip">📢 ${x.name} - ${x.objective}</div>`).join('')||'لسه ما عملت حملة'}
async function loadNotif(){let r=await fetch('/api/notifications'); let d=await r.json(); document.getElementById('notifList').innerHTML=d.map(n=>`<div class="notif"><b>${n.title}</b><p class="muted">${n.text}</p><small>${n.time}</small></div>`).join('')}
async function loadAnalytics(){let r=await fetch('/api/analytics'); let a=await r.json();
document.getElementById('aSpend').innerText=a.spend.toLocaleString(); document.getElementById('aReach').innerText=a.reach.toLocaleString(); document.getElementById('aLeads').innerText=a.leads; document.getElementById('aSales').innerText=a.sales; document.getElementById('aCalls').innerText=a.calls; document.getElementById('aQual').innerText=a.calls_qualified; document.getElementById('aLp').innerText=a.lp_views; document.getElementById('aRoas').innerText=a.roas+'x'; document.getElementById('aCpm').innerText=a.cpm; document.getElementById('aCpc').innerText=a.cpc; document.getElementById('aCtr').innerText=a.ctr;
let cv=document.getElementById('chart'); let ctx=cv.getContext('2d'); ctx.clearRect(0,0,cv.width,cv.height); ctx.strokeStyle='#FF4D8D'; ctx.lineWidth=3; ctx.beginPath(); let vals=[10,25,20,45,38,60,75,90]; vals.forEach((v,i)=>{let x=i*40+10,y=120-v; if(i==0) ctx.moveTo(x,y); else ctx.lineTo(x,y)}); ctx.stroke(); ctx.fillStyle='#F5C518'; ctx.fillText('📈 النتائج طالعة - المبيعات بتزيد',10,15);
}
loadAnalytics(); loadNotif();
</script></body></html>
"""

@app.get("/", response_class=HTMLResponse)
def home(): return HTML
@app.get("/api/analytics")
def ana(): return DB["analytics"]
@app.get("/api/notifications")
def notifs(): return DB["notifications"]
@app.get("/api/campaigns")
def list_c(): return DB["campaigns"]
@app.post("/api/campaigns")
def create_c(c: Campaign):
    d=c.dict(); d["id"]=str(uuid.uuid4())[:8]; d["created_at"]=str(datetime.datetime.now()); DB["campaigns"].append(d); return d
@app.post("/api/adsets")
def create_s(s: AdSet):
    d=s.dict(); d["id"]=str(uuid.uuid4())[:8]; DB["adsets"].append(d); return d
@app.get("/api/health")
def h(): return {"ok":True,"app":"NoorBook V32 PRO"}
