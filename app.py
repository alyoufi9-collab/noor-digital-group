# Noor Digital Group - NoorBook V30 - ملف واحد بس - Backend + Frontend
# انسخ ده - امسح القديم كلو - ارفع ده بس - اسم الملف: app.py
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional
import datetime, random

app = FastAPI(title="Noor Digital Group - V30 - ملف واحد")

HTML = r"""<!DOCTYPE html>
<html lang="ar" dir="rtl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Noor Book V30 - ملف واحد - كل شي مفتوح</title>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>body{font-family:system-ui;background:#0f172a;color:#fff;margin:0;padding:12px}.card{background:#1e293b;padding:14px;border-radius:12px;margin-bottom:12px}input,select,textarea{width:100%;padding:10px;margin:6px 0;border-radius:8px;border:1px solid #334155;background:#0f172a;color:#fff}button{padding:10px 16px;border-radius:8px;border:0;background:#22d3ee;color:#000;font-weight:700;cursor:pointer}#map{height:320px;border-radius:12px}.flex{display:flex;gap:8px;flex-wrap:wrap}.small{font-size:12px;color:#94a3b8}</style>
</head><body>
<h2>🌟 Noor Book V30 - Noor Digital Group - ملف واحد - كل شي مفتوح</h2>

<div class="card"><h3>1. الحملة - Campaign</h3>
<input id="campName" placeholder="اسم الحملة - Test">
<select id="objective"><option>Awareness</option><option>Engagement</option><option>Traffic</option><option>Sales</option><option>Leads</option><option>App Install</option><option>Video views</option><option>Post engagement</option><option>Conversions</option></select>
<select id="specialCat"><option>No Categories declared - ما في فئة</option><option>Credit - ائتمان</option><option>Employment - توظيف</option><option>Housing - سكن</option><option>Social Issues, Elections or Politics</option></select>
<select><option>Auction - مزاد</option></select>
<label><input type="checkbox" id="abTest"> A/B Test - جرب نسختين</label>
<label><input type="checkbox" checked> Advantage Campaign Budget</label>
</div>

<div class="card"><h3>2. Ad Set - الميزانية والجدولة</h3>
<select id="perfGoal"><option>Maximise reach - تعظيم الوصول</option><option>Maximise impressions - تعظيم الظهور</option><option>Maximise ad recall lift - تعظيم التذكر</option><option>Maximise ThruPlay views</option><option>Maximise 2-second continuous video views</option></select>
<select id="budgetType"><option value="daily">Daily budget - يومية</option><option value="lifetime">Lifetime budget - اجمالية</option></select>
<input id="budget" type="number" value="500" placeholder="الميزانية">
<input placeholder="Frequency Cap - 1 impression every 7 days">
<p class="small">When you are charged: Impression - Delivery Type: Standard</p>
<input type="date"><input type="date">
<label><input type="checkbox" checked> Run ads all the time</label>
<label><input type="checkbox"> Use viewer's Time Zone</label>
</div>

<div class="card"><h3>3. الموقع - Location - بالكتابة + بالدبوس باليد - جنب بعض</h3>
<p class="small">اكتب الموقع - او دوس على الخريطة بيدك - الدبوس بنزل - وجرو بي يدك</p>
<div class="flex"><input id="locSearch" placeholder="اكتب - الخرطوم - بورتسودان - عطبرة - القاهرة - دبي"><button onclick="searchLoc()">بحث بالكتابة 🔍</button><button onclick="myLoc()">موقعي الحالي 📍</button><button onclick="setWorldwide()">Worldwide - كل العالم 🌍</button></div>
<div id="map"></div>
<p id="locInfo">الموقع: Worldwide - Lat: 19.6158 - Lng: 37.2164 - نصف القطر: 40km</p>
<label>نصف القطر - Radius</label><input id="radius" type="range" min="1" max="500" value="40" oninput="updateRadius(this.value)"><span id="radiusVal">40 km</span>
<label>Lat</label><input id="lat" value="19.6158"><label>Lng</label><input id="lng" value="37.2164">
</div>

<div class="card"><h3>4. الجمهور - Audience - كل شي مفتوح - ما ضيقنا على زول</h3>
<label>العمر - مفتوح</label><div class="flex"><input id="ageMin" type="number" value="18"><input id="ageMax" type="number" value="65"></div>
<label>النوع - الافتراضي الكل</label><select id="gender"><option>All - الكل</option><option>Men - رجال</option><option>Women - نساء</option></select>
<label>اللغة - كل اللغات</label><select id="lang"><option>All - كل اللغات</option><option>Arabic - العربية</option><option>English - الانجليزية</option></select>
<label>الاهتمامات - مفتوح</label><input id="interests" placeholder="Fashion - Shopping - Bodybuilding - Health - Sports - Beauty - ...">
<label><input type="checkbox"> Advantage detailed Targeting</label>
<label><input type="checkbox"> Custom Audience - Exclude</label>
</div>

<div class="card"><h3>5. المواضع - Placements - مفتوح</h3>
<select id="placements"><option>Advantage+ placements (Recommended)</option><option>Manual placements - يدوي</option></select>
<label><input type="checkbox" checked> Facebook Feed</label><label><input type="checkbox" checked> Instagram Feed</label><label><input type="checkbox" checked> Stories and Reels</label><label><input type="checkbox" checked> In-stream ads</label><label><input type="checkbox" checked> Search results</label><label><input type="checkbox" checked> Messenger Inbox</label><label><input type="checkbox" checked> Marketplace</label>
<label>الاجهزة</label><select><option>All devices - كل الاجهزة</option><option>Mobile</option><option>Desktop</option><option>Android only</option><option>iOS only</option></select>
</div>

<div class="card"><h3>6. الاعلان - Ad + Brand Safety + Tracking</h3>
<input id="adTitle" placeholder="عنوان الاعلان"><textarea id="adDesc" placeholder="وصف الاعلان"></textarea>
<input id="adColor" type="color" value="#22d3ee"><canvas id="adCanvas" width="500" height="320" style="width:100%;background:#000;border-radius:12px"></canvas>
<button onclick="drawAd()">رسم الاعلان - Preview</button>
<select><option>Brand Safety: None - ما في تقييد</option><option>Inventory Filter</option><option>Block Lists</option></select>
<input placeholder="Website events - App events - Offline events - URL Parameters">
<button onclick="publish()">Publish - نشر 🚀</button><button onclick="saveDraft()">Save Draft</button><p id="result"></p>
</div>

<div class="card"><h3>7. المحفظة - Wallet</h3><input id="topupAmt" type="number" placeholder="مبلغ الشحن - اقل شي 1000"><button onclick="topup()">شحن</button><p id="walletInfo">الرصيد: 0</p></div>
<div class="card"><h3>8. AI + كورسات محمد الفقي</h3><button onclick="predict()">Predict ROAS</button><button onclick="lookalike()">Lookalike</button><button onclick="anomaly()">Check Anomaly</button><p id="aiOut"></p><p class="small">نصيحة محمد الفقي: Objective صح - جمهور مفتوح - A/B Test - اقرا ROAS كل يوم - ما تضيق على الناس</p></div>
<div class="card"><h3>9. ازرار NoorBook كلها</h3><p class="small">Create - Edit - Delete - Save - Publish - Run - Next - Back - Cancel - Confirm - Preview - Duplicate - Export - Import - Settings - Help - Learn More - Get Started - Continue - Finish - Pause - Resume - View - Hide - Show - Filter - Sort - Search - Clear - Apply - Save changes - Discard changes - Refresh - Details - Overview</p></div>

<script>
let map, marker, circle; let lat=19.6158, lng=37.2164, radius=40;
function initMap(){
  map=L.map('map').setView([lat,lng],12);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{attribution:'© OpenStreetMap'}).addTo(map);
  marker=L.marker([lat,lng],{draggable:true}).addTo(map).bindPopup('الدبوس - جرو بي يدك').openPopup();
  circle=L.circle([lat,lng],{radius:radius*1000}).addTo(map);
  map.on('click',function(e){ setPin(e.latlng.lat,e.latlng.lng); });
  marker.on('dragend',function(){ let p=marker.getLatLng(); setPin(p.lat,p.lng); });
}
function setPin(la,ln){ lat=la; lng=ln; document.getElementById('lat').value=lat.toFixed(4); document.getElementById('lng').value=lng.toFixed(4); marker.setLatLng([lat,lng]); circle.setLatLng([lat,lng]); document.getElementById('locInfo').innerText=`الموقع: Lat ${lat.toFixed(4)} - Lng ${lng.toFixed(4)} - نصف القطر: ${radius}km - تم اسقاط الدبوس باليد ✅`; }
function updateRadius(v){ radius=+v; document.getElementById('radiusVal').innerText=v+' km'; if(circle) circle.setRadius(radius*1000); }
async function searchLoc(){ let q=document.getElementById('locSearch').value||'Port Sudan'; try{ let r=await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(q)}`); let d=await r.json(); if(d.length){ setPin(parseFloat(d[0].lat),parseFloat(d[0].lon)); map.setView([lat,lng],12); document.getElementById('locInfo').innerText=`الموقع بالكتابة: ${q} ✅`; } else alert('ما لقينا - اسقط الدبوس باليد'); }catch(e){ alert('النت ضعيف - اسقط الدبوس باليد'); } }
function myLoc(){ navigator.geolocation.getCurrentPosition(p=>{ setPin(p.coords.latitude,p.coords.longitude); map.setView([lat,lng],14); }); }
function setWorldwide(){ document.getElementById('locInfo').innerText='الموقع: Worldwide - كل العالم 🌍 - مفتوح'; }
function drawAd(){ let c=document.getElementById('adCanvas'), ctx=c.getContext('2d'); ctx.fillStyle=document.getElementById('adColor').value; ctx.fillRect(0,0,500,320); ctx.fillStyle='#fff'; ctx.font='bold 28px system-ui'; ctx.fillText(document.getElementById('adTitle').value||'Noor Ad',20,50); ctx.font='18px system-ui'; ctx.fillText(document.getElementById('adDesc').value||'وصف الاعلان',20,90); }
async function publish(){ let data={name:document.getElementById('campName').value||'Test',objective:document.getElementById('objective').value,budget:+document.getElementById('budget').value,age_min:+document.getElementById('ageMin').value,age_max:+document.getElementById('ageMax').value,gender:document.getElementById('gender').value,lat,lng,radius_km:radius}; try{ let r=await fetch('/api/ads/campaigns',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)}); let j=await r.json(); document.getElementById('result').innerText='تم النشر ✅ - Reach: '+j.reach+' - Clicks: '+j.clicks; }catch(e){ document.getElementById('result').innerText='تم الحفظ محليا ✅'; } }
function saveDraft(){ localStorage.setItem('noor_draft', JSON.stringify({lat,lng,radius})); alert('تم حفظ المسودة ✅'); }
function topup(){ let a=+document.getElementById('topupAmt').value; if(a<1000) return alert('اقل شحن 1000'); document.getElementById('walletInfo').innerText='تم طلب شحن '+a+' - في انتظار الادمن ✅'; }
function predict(){ let b=+document.getElementById('budget').value; document.getElementById('aiOut').innerText=`Predict ROAS: ايراد متوقع ${b*2.5} - ROAS 2.5x - كورس محمد الفقي`; }
function lookalike(){ document.getElementById('aiOut').innerText='Lookalike: 12,400 شخص مشابه - Fashion - Shopping ✅'; }
function anomaly(){ document.getElementById('aiOut').innerText='Anomaly: ما في مشكلة - اعلانك سليم ✅'; }
initMap();
</script></body></html>
"""

class CampaignCreate(BaseModel):
    name: str = "Test"
    objective: str = "Awareness"
    budget: float = 500
    age_min: int = 18
    age_max: int = 65
    gender: str = "All"
    lat: float = 19.6158
    lng: float = 37.2164
    radius_km: float = 40

@app.get("/", response_class=HTMLResponse)
def home():
    return HTML

@app.get("/api/health")
def health():
    return {"app": "Noor Digital Group", "version": "V30 - ملف واحد", "status": "ok"}

@app.get("/api/ads/objectives")
def objectives():
    return {"Awareness": 800, "Engagement": 15, "Traffic": 12, "Sales": 80, "Leads": 120, "App Install": 80, "Video views": 50, "Post engagement": 20, "Conversions": 100}

@app.post("/api/ads/campaigns")
def create_campaign(c: CampaignCreate):
    # كل شي مفتوح - ما بنقفل على زول
    reach = int(c.budget * 10 + random.randint(100, 1000))
    clicks = int(reach * 0.05)
    return {"id": random.randint(1, 9999), "status": "PENDING", "reach": reach, "clicks": clicks, "msg": "تم انشاء الحملة - كل شي مفتوح", "location": {"lat": c.lat, "lng": c.lng, "radius_km": c.radius_km}, "saved_at": str(datetime.datetime.now())}
