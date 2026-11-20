# NoorBook V33 PRO MAX - Noor Digital Group - FINAL - كل الاكواد مجمعة
# زي ميتا بالظبط - ازرار + خوارزميات + واجهات + علاقات - بس اسماء وشعارات نور
# NoorBook / NoorSocial / NoorShot / NoorChat / NoorTalk / NoorMarket / Noor Pixel
# لا Facebook / Messenger / WhatsApp / Meta / Instagram نهائي
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List
import uuid, datetime
app = FastAPI(title="NoorBook V33 PRO MAX")
DB={"campaigns":[],"adsets":[],"ads":[],"drafts":[],"reports":[],"ad_accounts":[{"id":"ACT-001","name":"حساب اعلانات نور الرئيسي","balance":50000,"currency":"SDG","status":"ACTIVE"}],
"notifications":[{"id":"1","title":"✅ تمت الموافقة","text":"حملتك اتوافق عليها من الادمن - شغالة هسي","time":"قبل 5 دقايق"}],
"analytics":{"spend":125000,"reach":48200,"clicks":3210,"leads":187,"calls":96,"calls_qualified":61,"sales":34,"lp_views":2100,"ctr":6.6,"cpc":39,"cpm":2593,"roas":4.2}}
class Campaign(BaseModel):
    name: str; objective: str; special_category: str="none"; buying_type: str="Auction"
    spending_limit: float=0; ab_test: bool=False; advantage_budget: bool=True
    budget_type: str="lifetime"; budget: float=50000; status: str="DRAFT"
class AdSet(BaseModel):
    campaign_id: str=""; name: str=""; performance_goal: str="Maximise Reach"
    lat: float=15.5007; lng: float=32.5599; radius_km: int=25; location_name: str="الخرطوم"
    age_min: int=18; age_max: int=65; gender: str="all"; language: str="Arabic"
    detailed_targeting: str=""; custom_audience: str=""; lookalike_pct: int=1
    placements_mode: str="Advantage+"; placements: List[str]=[]
    device_type: str="All devices"; connection_type: str="All connections"
    android_min: str="Any"; ios_min: str="Any"
    budget: float=10000; schedule_type: str="grid"; week_grid: List[List[int]]=[]
    start_date: str=""; end_date: str=""; timezone_mode: str="Khartoum Time"
    frequency_cap: str="1 every 7 days"; bid_control: str="Highest Volume"
    dynamic_creative: bool=False; brand_safety: str="Standard"
class Ad(BaseModel):
    adset_id: str=""; name: str=""; format: str="carousel"; identity_page: str="NoorSocial Page"
    headline: str=""; primary_text: str=""; cta: str="تسوق الان"; media_urls: List[str]=[]
    destination: str="NoorMarket"; url_params: str=""; tracking: str="Noor Pixel"
    status: str="PENDING_REVIEW"

HTML = r"""
<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>NoorBook PRO MAX</title>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"><script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>
*{box-sizing:border-box;font-family:system-ui}body{margin:0;background:#0B0714;color:#fff;padding-bottom:110px}
.top{position:sticky;top:0;z-index:20;background:rgba(15,8,30,.92);backdrop-filter:blur(12px);padding:12px 16px;display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #2A1A4A}
.logo{font-weight:900;font-size:21px;background:linear-gradient(90deg,#F5C518,#FF4D8D,#7C3AED);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.pill{background:linear-gradient(90deg,#7C3AED,#FF4D8D);padding:8px 12px;border-radius:999px;font-size:12px;font-weight:700}
.tabs{display:flex;gap:8px;padding:10px 16px;overflow:auto}.tab{white-space:nowrap;background:#1A1130;border:1px solid #2A1A4A;padding:9px 13px;border-radius:999px;font-size:12px}.tab.on{background:linear-gradient(90deg,#7C3AED,#FF4D8D);font-weight:800}
.card{background:linear-gradient(180deg,#1B1233,#120B24);border:1px solid #2A1A4A;border-radius:20px;padding:16px;margin:12px 16px}
.muted{color:#B9AEE0;font-size:13px;line-height:1.7}label{display:block;font-size:13px;margin:13px 0 6px;color:#E7DEFF}
input,select,textarea{width:100%;background:#0F0A1F;border:1px solid #35245E;color:#fff;padding:12px;border-radius:14px;font-size:14px}
.obj-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px}.obj{border:2px solid #35245E;background:#17102E;padding:12px;border-radius:16px;cursor:pointer}.obj.sel{border-color:#F5C518;background:#2A1F08}.algo{font-size:11px;color:#F5C518}
.btn{width:100%;background:linear-gradient(90deg,#F5C518,#FF4D8D,#7C3AED);border:0;padding:14px;border-radius:16px;font-weight:900;color:#fff;margin-top:12px}
.btn2{background:#241640;border:1px solid #35245E;color:#fff;padding:9px 13px;border-radius:12px}.chip{display:inline-block;background:#241640;border:1px solid #35245E;padding:6px 10px;border-radius:999px;font-size:12px;margin:3px}
.kpi{display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:8px}.kpi div{background:#0F0A1F;border:1px solid #2A1A4A;border-radius:14px;padding:10px;text-align:center}.kpi b{color:#F5C518}
.hide{display:none}.steps{display:flex;gap:8px;padding:0 16px}.step{flex:1;text-align:center;background:#1A1130;padding:9px;border-radius:12px;font-size:11px}.step.on{background:#F5C518;color:#000;font-weight:800}
.grid-wrap{overflow:auto;border:1px solid #35245E;border-radius:14px;background:#0F0A1F;padding:8px}table.grid{border-collapse:collapse;font-size:11px}table.grid td{border:1px solid #2A1A4A}.cell{width:26px;height:26px;background:#1A1130;cursor:pointer}.cell.on{background:linear-gradient(135deg,#F5C518,#FF4D8D)}
#map{height:260px;border-radius:16px;border:1px solid #35245E}.notif{background:#0F0A1F;border:1px solid #2A1A4A;border-radius:14px;padding:12px;margin-top:10px}
.carousel{display:flex;gap:10px;overflow:auto}.car{flex:0 0 140px;background:#0F0A1F;border:1px solid #35245E;border-radius:16px;padding:10px;text-align:center}
.nav{position:fixed;bottom:0;right:0;left:0;background:#120B24;border-top:1px solid #2A1A4A;display:flex;padding:11px}.nav div{flex:1;text-align:center;font-size:11px;color:#B9AEE0}.nav div.on{color:#F5C518;font-weight:900}
canvas{width:100%;height:130px;background:#0F0A1F;border-radius:14px}
</style></head><body>
<div class="top"><div class="logo">N • NoorBook PRO MAX</div><div><span>🌐 <select id="uiLang" onchange="alert('تم تغيير لغة الواجهة: '+this.value+' - الواجهة عربي / انجليزي فقط - لغة الاعلان اي لغة')"><option>العربية - Arabic</option><option>English - الانجليزية</option></select></span> <span class="pill">💰 <span id="wallet">50,000</span> ج.س 🔔 3</span></div></div>
<div class="tabs">
<div class="tab on" onclick="showTab('dash',this)">📊 لوحة التحكم</div><div class="tab" onclick="showTab('create',this)">📢 انشاء - Create</div><div class="tab" onclick="showTab('aud',this)">👥 جمهور</div><div class="tab" onclick="showTab('ads',this)">🖼️ الاعلانات</div><div class="tab" onclick="showTab('draft',this)">📝 مسودات</div><div class="tab" onclick="showTab('rep',this)">📄 تقارير</div><div class="tab" onclick="showTab('acct',this)">🏦 حسابات + فوترة</div><div class="tab" onclick="showTab('admin',this)">🛡️ مراجعة الادمن</div><div class="tab" onclick="showTab('auto',this)">🤖 اوتومايشن + بكسل</div><div class="tab" onclick="showTab('notif',this)">🔔 اشعارات</div>
</div>
<div id="tab-dash"><div class="card"><h3>📊 تحليل البيانات - Analytics - زي ميتا</h3><div class="kpi"><div><b id="aSpend">-</b><br><small>الصرف</small></div><div><b id="aReach">-</b><br><small>الوصول</small></div><div><b id="aLeads">-</b><br><small>ليدز</small></div><div><b id="aSales">-</b><br><small>مبيعات</small></div></div><div class="kpi" style="margin-top:8px"><div><b id="aCalls">-</b><br><small>مكالمات</small></div><div><b id="aQual">-</b><br><small>مكالمات +3 دقايق</small></div><div><b id="aLp">-</b><br><small>لانديق بيج فيوز</small></div><div><b id="aRoas">-</b><br><small>ROAS</small></div></div><p class="muted">CPM <b id="aCpm"></b> | CPC <b id="aCpc"></b> | CTR <b id="aCtr"></b>% | تكلفة الليد = الصرف / الليدز | تكلفة المبيعة = الصرف / المبيعات | مكالمة اقل من 3 دقايق = ما مبيعة - 3 دقايق واكتر = مبيعة مؤهلة</p><canvas id="chart"></canvas></div></div>
<div id="tab-create" class="hide">
<div class="steps"><div class="step on" id="st1">1 - الحملة</div><div class="step" id="st2">2 - المجموعة</div><div class="step" id="st3">3 - الاعلان</div><div class="step" id="st4">4 - مراجعة ونشر</div></div>
<div id="step1"><div class="card"><h3>1 - الحملة - Campaign - Create</h3>
<label>اسم الحملة - Campaign Name</label><input id="campName" placeholder="Test - عطور عطبرة">
<label>فئات الاعلانات الخاصة - Special Ad Categories</label><select id="specCat"><option value="none">No Categories Declared - لم يتم الاعلان عن اي فئات</option><option>Credit - الائتمان - قروض - تمويل</option><option>Employment - التوظيف - عروض عمل - تدريب</option><option>Housing - السكن - عقارات - رهن</option><option>Social Issues, Elections or Politics - قضايا اجتماعية - انتخابات - سياسة</option></select><p class="muted">اعلن عشان ما يتم رفض اعلانك او يتحظر</p>
<label>هدف الحملة - 6 اهداف - Campaign Objective</label><div class="obj-grid" id="objs"></div>
<label>تفاصيل الحملة - Campaign Details</label><select><option>Buying Type: Auction - مزاد</option></select>
<label>حد انفاق الحملة - Add Campaign Spending Limit</label><input type="number" placeholder="مثال: 200000 - اختياري">
<label><input type="checkbox" id="ab"> A/B Test - انشاء اختبار A/B - اختبر نسخ بفروق مختلفة - صور - نصوص - جمهور - اماكن ظهور - كل نسخة حتظهر لجزء منفصل من جمهورك</label>
<div id="abBox" class="hide"><label>نسخة A</label><input value="نسخة A - صورة"><label>نسخة B</label><input value="نسخة B - فيديو"><p class="muted">50% / 50% - بعد 1000 ظهور - الخوارزمية تختار الفايز</p></div>
<label><input type="checkbox" id="adv" checked> Advantage Campaign Budget - ميزانية Advantage - حتوزع ميزانيتك عبر المجموعات الشغالة - للحصول على مزيد من النتائج</label>
<div style="display:flex;gap:10px"><div style="flex:1"><label>نوع الميزانية</label><select id="bType"><option>Lifetime - مدى الحياة - لازم للجدولة</option><option>Daily - يومية</option></select></div><div style="flex:1"><label>الميزانية ج.س</label><input id="campBudget" type="number" value="50000"></div></div>
<button class="btn" onclick="gotoStep(2)">التالي - Next →</button></div></div>
<div id="step2" class="hide"><div class="card"><h3>2 - المجموعة - Ad Set - New Awareness Ad Set</h3>
<label>اسم المجموعة - Ad Set Name</label><input id="setName" value="مجموعة 1 - الخرطوم">
<label>هدف الاداء - Performance Goal</label><select id="perf"><option>Maximise Reach - تعظيم الوصول</option><option>Maximise Impressions - تعظيم الظهور</option><option>Maximise Ad Recall Lift - تعظيم تذكر الاعلان</option><option>Maximise ThruPlay Views - مشاهدات ThruPlay - الفيديو كلو او 15 ثانية</option><option>Maximise 2-Second Views - مشاهدات 2 ثانية - 50% بكسلات ظاهرة</option><option>Purchase - شراء</option><option>Add to Cart - اضافة للسلة</option><option>Lead - ليد</option><option>Qualified Call +3 min - مكالمة مؤهلة</option><option>Landing Page View - لانديق بيج فيو - قعد 10 ثواني</option><option>Link Click - نقرة رابط</option></select>
<p class="muted">Bid Control: نور حتحاول تصرف ميزانيتك كاملة وتجيب اكبر عدد من الظهور - 1000 ظهور - Highest Volume | Frequency Cap: 1 ظهور كل 7 ايام | Delivery Type: Standard | When you are charged: Impression</p>
<label>📍 اللوكيشن الحقيقي - Drop a Pin - اسقط الدبوس - جرو باليد</label><p class="muted">جر الدبوس الاحمر - وين ما تحتو - ده جمهورك - Zoom out / Zoom in</p><div id="map"></div><p class="muted">المكان: <b id="locLabel">الخرطوم - السودان</b> | Lat <b id="latV">15.5007</b> | Lng <b id="lngV">32.5599</b></p>
<label>نصف القطر - Radius</label><input type="range" min="1" max="80" value="25" oninput="document.getElementById('radV').innerText=this.value"><span><b id="radV">25</b> كم حول الدبوس</span>
<div style="display:flex;gap:8px;margin-top:8px"><button class="btn2" onclick="goLoc(15.5007,32.5599,'الخرطوم')">الخرطوم</button><button class="btn2" onclick="goLoc(17.6784,33.9715,'عطبرة')">عطبرة</button><button class="btn2" onclick="goLoc(19.6158,37.2164,'بورتسودان')">بورتسودان</button><button class="btn2" onclick="goLoc(30.0444,31.2357,'القاهرة +40 كم')">القاهرة</button></div>
<label>اضافة مواقع بالجملة - Add Locations in Bulk / اضافة عالمي - Add Worldwide</label><input placeholder="مثال: الخرطوم - عطبرة - القاهرة">
<div style="display:flex;gap:10px"><div style="flex:1"><label>العمر من - Age</label><input type="number" value="18" id="ageMin"></div><div style="flex:1"><label>العمر لي</label><input type="number" value="65" id="ageMax"></div></div><p class="muted">كل شي مفتوح بدون تقييد - اختار اي عمر - اختيار جمهور تحت 18 سيحد من خيارات الاستهداف</p>
<label>الجنس - Gender</label><select><option>All - الكل</option><option>Men - رجال</option><option>Women - النساء</option></select>
<label>لغة الاعلان - Language of Ad - اي لغة من لغات العالم</label><select><option>Arabic - العربية</option><option>English - الانجليزية</option><option>French - الفرنسية</option><option>Spanish - الاسبانية</option><option>Turkish - التركية</option><option>Amharic - الامهرية</option><option>Swahili - السواحيلية</option><option>Urdu - الاوردو</option><option>Hindi - الهندية</option></select><p class="muted">لغة الواجهة: عربي / انجليزي فقط - لغة الاعلان: حسب لغة العميل او اختيار اجباري - اي لغة</p>
<label>الاستهداف التفصيلي - Detailed Targeting</label><input placeholder="Add demographics, interests or behaviours"><div><span class="chip">Online Shopping - التسوق الالكتروني</span><span class="chip">Jewellery - المجوهرات</span><span class="chip">Clothing - الملابس</span><span class="chip">Shopping - التسوق</span><span class="chip">Engaged Shoppers - المتسوقون المتفاعلون</span><span class="chip">Handbags - الحقائب</span><span class="chip">Dresses - فساتين</span><span class="chip">Luxury Goods - السلع الفاخرة</span><span class="chip">Necklace - قلادة</span><span class="chip">Ring - خاتم</span><span class="chip">Beauty - الجمال</span><span class="chip">Fashion - الموضة</span><span class="chip">Health & Wellness - الصحة</span><span class="chip">Bodybuilding - كمال الاجسام</span></div>
<label>اماكن الظهور - Placements</label><select><option>Advantage+ Placements - مواضع Advantage+ - الموصى بها</option><option>Manual Placements - المواضع اليدوية - اختر يدويا</option></select><div><span class="chip">✅ NoorSocial Feed</span><span class="chip">✅ NoorShot Feed / Reels / Explore</span><span class="chip">✅ NoorChat Inbox</span><span class="chip">✅ NoorMarket</span><span class="chip">✅ NoorTalk</span><span class="chip">✅ Feeds</span><span class="chip">✅ Stories and Reels</span><span class="chip">✅ In-stream</span><span class="chip">✅ Search</span><span class="chip">✅ Messages</span><span class="chip">✅ Apps and Sites</span></div>
<label>📱 الاجهزة - Devices - وين يظهر الاعلان؟ - مثل ميتا - كامل</label>
<select id="deviceType" onchange="toggleDeviceOptions()"><option value="all">All devices - جميع الاجهزة - الموصى بها</option><option value="mobile">All mobile devices - جميع الاجهزة المحمولة</option><option value="android">Android devices only - اجهزة اندرويد فقط</option><option value="ios">iOS devices only - اجهزة iOS فقط - ايفون</option><option value="desktop">Desktop only - كمبيوتر فقط</option><option value="feature">Feature phones only - الهواتف العادية فقط</option></select>
<div style="background:#0F0A1F;border:1px solid #35245E;border-radius:14px;padding:12px;margin-top:10px">
<label>نوع الاتصال - Connection - مثل ميتا</label>
<select id="connectionType"><option value="all">All connections - كل الاتصالات - واي فاي + شبكة عادية</option><option value="wifi">Only when connected to Wi-Fi - فقط عند الاتصال بالواي فاي - اعلانك ما حيظهر لو الزول شغال ببيانات</option><option value="cellular">Cellular only - شبكة عادية فقط - بيانات الجوال - 3G / 4G / 5G - بدون واي فاي</option><option value="wifi_cellular">Wi-Fi + Cellular - واي فاي + شبكة - الاثنين</option></select>
<p class="muted">💡 لو اعلانك فيديو تقيل - اختار Wi-Fi بس - عشان الزول ما يزهج - لو صورة خفيفة - اختار الكل</p>
<div style="display:flex;gap:10px"><div style="flex:1"><label>اصدار اندرويد - Min - ادنى</label><select><option>اي اصدار - Any</option><option>Android 8.0 واعلى</option><option>Android 10 واعلى</option><option>Android 12 واعلى</option><option>Android 13 واعلى</option><option>Android 14 واعلى</option></select></div><div style="flex:1"><label>اصدار اندرويد - Max - اقصى</label><select><option>اي اصدار - Any</option><option>Android 14</option><option>Android 15</option></select></div></div>
<div style="display:flex;gap:10px"><div style="flex:1"><label>اصدار iOS - Min - ادنى</label><select><option>اي اصدار - Any</option><option>iOS 14 واعلى</option><option>iOS 15 واعلى</option><option>iOS 16 واعلى</option><option>iOS 17 واعلى</option><option>iOS 18 واعلى</option></select></div><div style="flex:1"><label>اصدار iOS - Max - اقصى</label><select><option>اي اصدار - Any</option><option>iOS 18</option><option>iOS 19</option></select></div></div>
<label>اجهزة محمولة محددة - Specific mobile devices & OS</label><select><option>All - الكل</option><option>Samsung - سامسونج</option><option>iPhone - ايفون</option><option>Huawei - هواوي</option><option>Xiaomi - شاومي</option><option>Tecno - تكنو</option><option>Infinix - انفينيكس</option></select>
<p class="muted" style="background:#241640;padding:10px;border-radius:10px">- Android + Wi-Fi = اعلانك لناس عندها اندرويد ومتصلة بواي فاي بس - رخيص - CPM رخيص<br>- iOS only = ناس اقل - لكن قروشهم اكتر - CPM اغلى - مناسب للعطور الغالية<br>- All devices = الخوارزمية تختار ارخص نتيجة وتوزع الميزانية هناك - Advantage</p>
</div>
<label>سلامة العلامة - Brand Safety</label><select><option>Standard - قياسي</option><option>Inventory Filter - تصفية المخزون</option><option>Block Lists - قوائم الحظر</option><option>Content Type Exclusions - استبعاد نوع المحتوى</option></select>
</div><div class="card"><h3>🗓️ الجدولة - مربعات تظلل - زي ميتا</h3><p class="muted">دوس يتلون - دوس تاني يطفي - اسحب تظلل كتير - الجدولة متاحة فقط مع Lifetime Budget</p><div style="display:flex;gap:8px;margin-bottom:8px"><button class="btn2" onclick="gridAll()">كل الاسبوع</button><button class="btn2" onclick="gridPeak()">ذروة 6م-11م</button><button class="btn2" onclick="gridClear()">امسح كلو</button></div><div class="grid-wrap"><table class="grid" id="gridTable"></table></div><p class="muted"><b id="gridHours">0</b> ساعة شغالة من 168 | توقيت: <select><option>Use viewer's Time Zone - توقيت المشاهد</option><option>Use this ad account's Time Zone - Khartoum Time - توقيت الخرطوم</option></select> | بداية <input type="date"> نهاية <input type="date"></p></div>
<div style="display:flex;gap:10px;padding:0 16px"><button class="btn2" style="flex:1" onclick="gotoStep(1)">← Back - رجوع</button><button class="btn" style="flex:2" onclick="gotoStep(3)">التالي - Next →</button></div></div>
<div id="step3" class="hide"><div class="card"><h3>3 - الاعلان - Ad - Create Ad</h3>
<label>اسم الاعلان - Ad Name</label><input value="New Awareness Ad">
<label>الهوية - Identity - Partnership Ad</label><select><option>NoorSocial Page - صفحة نور</option><option>NoorShot Account - حساب نور شوت</option></select>
<label>اعداد الاعلان - Ad Setup</label><select><option>Create Ad - انشاء اعلان</option><option>Use Existing Post - استخدم المنشور الحالي</option><option>Use Creative Hub Mockup - استخدم نموذج Hub</option></select>
<label>صيغة الاعلان - Format</label><select id="adFormat"><option>Carousel - كاراسول - اكتر من صورة</option><option>Single Image - صورة واحدة</option><option>Video - فيديو</option><option>Reels - ريلز</option><option>Collection - مجموعة</option></select>
<label>رفع الاعلان - صور او فيديو او ريلز - ملفات او روابط</label><input type="file" accept="image/*,video/*" multiple onchange="alert('تم رفع الملفات ✅ - '+this.files.length+' ملف')"><input placeholder="او الصق رابط صورة / فيديو - https://..." style="margin-top:8px"><div class="carousel"><div class="car"><img src="https://via.placeholder.com/140"><b>بطاقة 1</b><input placeholder="عنوان 1"><input placeholder="رابط 1"></div><div class="car"><img src="https://via.placeholder.com/140"><b>بطاقة 2</b><input placeholder="عنوان 2"><input placeholder="رابط 2"></div><div class="car"><img src="https://via.placeholder.com/140"><b>بطاقة 3</b><input placeholder="عنوان 3"><input placeholder="رابط 3"></div><div class="car" style="display:flex;align-items:center;justify-content:center;font-size:30px">+</div></div>
<label>العنوان - Headline</label><input placeholder="عطور اصلية - توصيل عطبرة"><label>النص - Primary Text</label><textarea placeholder="اكتب نص يجذب المهتم - ما الفضولي..."></textarea>
<label>زر الدعوة - CTA</label><select><option>تسوق الان</option><option>اعرف المزيد</option><option>ارسل رسالة - NoorChat</option><option>اتصل - NoorTalk</option><option>سجّل الان</option><option>حمّل التطبيق</option></select>
<label>وجهة الاعلان - Destination - Landing Page</label><select><option>NoorMarket - متجر</option><option>NoorSocial - صفحة</option><option>NoorChat - دردشة</option><option>صفحة هبوط خارجية</option></select>
<label>التتبع - Tracking - Noor Pixel</label><select><option>Website Events - احداث الموقع - Set up</option><option>App Events - احداث التطبيق - Set up</option><option>Offline Events - احداث غير متصلة - Set up</option></select>
<label>معلمات URL - URL Parameters</label><input placeholder="utm_source=noorbook&utm_campaign=عطور">
<label><input type="checkbox" id="dyn"> Dynamic Creative - الابداع الديناميكي - حنولد تركيبات محسّنة تلقائيا</label>
<div style="display:flex;gap:10px"><button class="btn2" style="flex:1" onclick="gotoStep(2)">← Back</button><button class="btn" style="flex:2" onclick="gotoStep(4)">مراجعة - Review →</button></div></div></div>
<div id="step4" class="hide"><div class="card"><h3>4 - مراجعة ونشر - Review & Publish</h3><p class="muted" id="reviewText">...</p>
<label>حفظ كـ؟</label><select id="saveAs"><option value="publish">نشر - Publish - يمشي للادمن للمراجعة</option><option value="draft">مسودة - Draft</option></select>
<button class="btn" onclick="doPublish()">🚀 نشر - Publish</button><p class="muted">بالنقر على نشر - فأنت توافق على شروط نور وارشادات اعلان نور</p>
<button class="btn2" style="width:100%" onclick="saveDraft()">💾 حفظ كمسودة - Save Draft</button><button class="btn2" style="width:100%;margin-top:8px" onclick="gotoStep(3)">← Back</button></div></div>
</div>
<div id="tab-aud" class="hide"><div class="card"><h3>👥 الجمهور المخصص - Custom Audience</h3><select><option>شافو الفيديو - Video Viewers</option><option>زارو الموقع - Noor Pixel</option><option>بعتو رسالة - NoorChat</option><option>اتصلو +3 دقايق - NoorTalk</option><option>ارقام تلفونات - Phone Numbers</option><option>اشترو قبل كده - Purchasers</option></select><label>المدة</label><select><option>اخر 7 ايام</option><option>اخر 30 يوم</option><option>اخر 90 يوم</option><option>اخر 365 يوم</option></select><button class="btn2" style="width:100%" onclick="alert('تم حفظ الجمهور المخصص ✅')">حفظ الجمهور المخصص</button></div><div class="card"><h3>🧬 الجمهور المشابه - Lookalike</h3><label>نسبة التشابه</label><input type="range" min="1" max="10" value="1" oninput="document.getElementById('lookV').innerText=this.value+'%'"><p><b id="lookV">1%</b> - 1% تشابه قوي - 10% واسع</p><button class="btn2" style="width:100%" onclick="alert('تم انشاء جمهور مشابه ✅')">انشاء جمهور مشابه</button></div></div>
<div id="tab-ads" class="hide"><div class="card"><h3>🖼️ مكتبة الاعلانات - Ads Library</h3><div id="adsList"><p class="muted">لسه ما عملت اعلان</p></div><p class="muted">تقدر: حفظ - مسح - اعادة استخدام - تعديل - تكرار - Duplicate - تصدير - Export - استيراد - Import</p><div style="display:flex;gap:8px"><button class="btn2" onclick="alert('تم تكرار الاعلان ✅')">Duplicate - تكرار</button><button class="btn2" onclick="alert('تم تصدير الاعلان ✅')">Export - تصدير</button><button class="btn2" onclick="alert('تم حفظ الاعلان ✅')">Save - حفظ</button></div></div></div>
<div id="tab-draft" class="hide"><div class="card"><h3>📝 المسودات - Drafts</h3><div id="draftList"><p class="muted">لا توجد مسودات</p></div></div></div>
<div id="tab-rep" class="hide"><div class="card"><h3>📄 التقارير - Reports</h3><label>اختر الزمن</label><select><option>اليوم</option><option>اخر 7 ايام</option><option>اخر 30 يوم</option><option>مخصص - Custom</option></select><button class="btn2" style="width:100%" onclick="alert('تم حفظ التقرير ✅')">حفظ التقرير - Save Report</button><button class="btn2" style="width:100%;margin-top:8px" onclick="alert('تم مسح التقرير ✅')">مسح التقرير - Delete Report</button><div id="repList"></div></div></div>
<div id="tab-acct" class="hide"><div class="card"><h3>🏦 حسابات الاعلانات - Ad Accounts</h3><div id="acctList"></div><button class="btn2" style="width:100%" onclick="alert('تم ارسال طلب حساب اعلان جديد للادمن ✅')">طلب حساب اعلان جديد - يمشي للادمن</button><p class="muted">الدفع لانشاء الاعلانات عن طريق طلب من الادمن - هو المتصرف</p></div><div class="card"><h3>💳 الفوترة وعمليات الدفع - Billing - في الاعدادات</h3><p class="muted">الاعدادات - Settings: اسم الحساب - العملة SDG - طريقة الدفع - بنكك - رصيد - فواتير - حدود الانفاق - اشعارات الدفع</p><label>طريقة الدفع</label><select><option>بنكك - Bankak</option><option>محفظة نور - Noor Wallet</option><option>بطاقة - Card</option></select><label>المبلغ للشحن</label><input type="number" value="50000"><button class="btn" onclick="alert('تم ارسال طلب شحن للادمن ✅')">طلب شحن - يمشي للادمن</button></div></div>
<div id="tab-admin" class="hide"><div class="card"><h3>🛡️ مراجعة الادمن - Admin Review</h3><p class="muted">الادمن هو المتصرف - هو البيوافق - يرفض - يوقف - كل اعلان لازم يمر على الادمن</p><div id="adminList"><p class="muted">لا توجد اعلانات معلقة</p></div></div></div>
<div id="tab-auto" class="hide"><div class="card"><h3>🤖 اوتومايشن + ماشين ليرنينج + بكسل</h3><p class="muted">Noor Pixel: كود تتبع في موقعك - بيعرف مين زار - مين اشترى - مين ساب السلة - والخوارزمية بتتعلم وتحسن الاعلان تلقائيا</p><label>كود البكسل - Noor Pixel ID</label><input value="NOOR-PIXEL-123456 - انسخو وحطو في موقعك"><label><input type="checkbox" checked> Automation - اوتومايشن - لو الليد ما رد في 10 دقايق - ابعت ليهو رسالة تلقائية</label><label><input type="checkbox" checked> Machine Learning - ماشين ليرنينج - الخوارزمية تتعلم من المبيعات</label></div><div class="card"><h3>💬 الرد التلقائي للرسائل - Auto Reply - NoorChat</h3><label>رسالة الترحيب التلقائية</label><textarea>اهلا بيك في متجرنا - عايز شنو؟ عطور - ملابس - عقارات - حنرد عليك في دقيقة</textarea><label>لو العميل قال: كم السعر؟</label><input value="السعر 15000 ج.س - التوصيل مجاني - عايز تطلب؟"><button class="btn2" style="width:100%" onclick="alert('تم حفظ الرد التلقائي ✅')">حفظ الرد التلقائي</button></div></div>
<div id="tab-notif" class="hide"><div class="card"><h3>🔔 اشعارات وتنبيهات</h3><div id="notifList"></div><p class="muted">البلاغات بخصوص الاعلانات - التقارير: اعلانك اتوافق - اترفض - ميزانيتك خلصت - جاك ليد جديد</p></div></div>
<div class="nav"><div class="on" onclick="showTab('dash',this)">🏠 الرئيسية</div><div onclick="showTab('create',this)">📢 انشاء</div><div onclick="showTab('aud',this)">👥 جمهور</div><div onclick="showTab('notif',this)">🔔 اشعارات</div><div onclick="showTab('acct',this)">⚙️ اعدادات</div></div>
<script>
const OBJS=[{id:'AWARENESS',t:'الوعي - Awareness',d:'ناس تتذكر',a:'الخوارزمية: تدور على ناس بتتذكر - Reach / Impressions / Recall'},{id:'TRAFFIC',t:'الزيارات - Traffic',d:'ناس تدوس',a:'الخوارزمية: تدور على ناس بتدوس - Link Click / Landing Page View / NoorChat / Calls'},{id:'ENGAGEMENT',t:'التفاعل - Engagement',d:'لايك - تعليق',a:'الخوارزمية: تدور على ناس بتتفاعل - Messages / Video Views / Post Engagement'},{id:'LEADS',t:'ليدز - Leads',d:'فورم - رسالة',a:'الخوارزمية: تدور على ناس بتملا بيانات - Instant Forms / Calls / NoorChat'},{id:'APP',t:'تطبيق - App',d:'تحميل',a:'الخوارزمية: تدور على ناس بتنزل - App Installs / App Events'},{id:'SALES',t:'مبيعات - Sales',d:'شراء',a:'الخوارزمية: تدور على ناس بتشتري - Purchase / Add to Cart / Catalogue / NoorChat / Calls - لازم Noor Pixel'}];
let sel='SALES';
function renderObjs(){document.getElementById('objs').innerHTML=OBJS.map(o=>`<div class="obj ${o.id==sel?'sel':''}" onclick="sel='${o.id}';renderObjs()"><b>${o.t}</b><small>${o.d}</small><div class="algo">${o.a}</div></div>`).join('')}renderObjs();
function showTab(id,el){['dash','create','aud','ads','draft','rep','acct','admin','auto','notif'].forEach(x=>document.getElementById('tab-'+x).classList.toggle('hide',x!==id)); document.querySelectorAll('.tab').forEach(t=>t.classList.remove('on')); if(el) el.classList.add('on'); if(id=='notif') loadNotif(); if(id=='acct') loadAcct(); if(id=='admin') loadAdmin(); if(id=='ads') loadAds();}
function gotoStep(n){[1,2,3,4].forEach(i=>{document.getElementById('step'+i).classList.toggle('hide',i!==n); document.getElementById('st'+i).classList.toggle('on',i===n)}); if(n==4){document.getElementById('reviewText').innerHTML='الحملة: '+(document.getElementById('campName').value||'Test')+'<br>الهدف: '+sel+'<br>المجموعة: '+document.getElementById('setName').value+'<br>المكان: '+document.getElementById('locLabel').innerText+'<br>الجدول: '+document.getElementById('gridHours').innerText+' ساعة في الاسبوع<br>الجهاز: '+document.getElementById('deviceType').value+'<br>الاتصال: '+document.getElementById('connectionType').value+'<br>الاداء: '+document.getElementById('perf').value}}
document.getElementById('ab').addEventListener('change',e=>document.getElementById('abBox').classList.toggle('hide',!e.target.checked));
let map=L.map('map').setView([15.5007,32.5599],12); L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:19}).addTo(map);
let marker=L.marker([15.5007,32.5599],{draggable:true}).addTo(map); let circle=L.circle([15.5007,32.5599],{radius:25000,color:'#FF4D8D',fillColor:'#FF4D8D',fillOpacity:.15}).addTo(map);
marker.on('dragend',()=>{let p=marker.getLatLng(); document.getElementById('latV').innerText=p.lat.toFixed(4); document.getElementById('lngV').innerText=p.lng.toFixed(4); document.getElementById('locLabel').innerText='مكان مخصص - '+p.lat.toFixed(4)+','+p.lng.toFixed(4); circle.setLatLng(p)});
function goLoc(lat,lng,name){map.setView([lat,lng],12); marker.setLatLng([lat,lng]); circle.setLatLng([lat,lng]); document.getElementById('locLabel').innerText=name+' - السودان'; document.getElementById('latV').innerText=lat; document.getElementById('lngV').innerText=lng}
let grid=[]; function initGrid(){grid=Array.from({length:7},()=>Array(24).fill(1)); renderGrid()}
function renderGrid(){let days=['السبت','الاحد','الاثنين','الثلاثاء','الاربعاء','الخميس','الجمعة']; let h='<tr><th>اليوم</th>'+Array.from({length:24},(_,i)=>`<th>${i}</th>`).join('')+'</tr>'; h+=days.map((d,di)=>'<tr><th>'+d+'</th>'+Array.from({length:24},(_,hi)=>`<td><div class="cell ${grid[di][hi]?'on':''}" onclick="toggleCell(${di},${hi})"></div></td>`).join('')+'</tr>').join(''); document.getElementById('gridTable').innerHTML=h; document.getElementById('gridHours').innerText=grid.flat().reduce((a,b)=>a+b,0)}
function toggleCell(d,h){grid[d][h]=grid[d][h]?0:1; renderGrid()} function gridAll(){grid=Array.from({length:7},()=>Array(24).fill(1)); renderGrid()} function gridPeak(){grid=Array.from({length:7},()=>Array.from({length:24},(_,h)=>(h>=18&&h<23)?1:0)); renderGrid()} function gridClear(){grid=Array.from({length:7},()=>Array(24).fill(0)); renderGrid()} initGrid();
function toggleDeviceOptions(){let v=document.getElementById('deviceType').value; if(v=='android') alert('تم اختيار: اندرويد فقط - اعلانك حيظهر لاندرويد بس'); if(v=='ios') alert('تم اختيار: ايفون فقط - اعلانك حيظهر لايفون بس')}
async function doPublish(){let camp={name:document.getElementById('campName').value||'Test',objective:sel,ab_test:document.getElementById('ab').checked}; let r=await fetch('/api/campaigns',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(camp)}); let c=await r.json(); let ad={name:'New Awareness Ad',format:'carousel'}; await fetch('/api/ads',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(ad)}); alert('✅ تم ارسال الاعلان للادمن للمراجعة - استنى الموافقة'); showTab('admin',null)}
async function saveDraft(){let d={name:document.getElementById('campName').value||'مسودة بدون اسم',objective:sel}; await fetch('/api/drafts',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(d)}); alert('💾 تم حفظ المسودة ✅'); showTab('draft',null)}
async function loadNotif(){let r=await fetch('/api/notifications'); let d=await r.json(); document.getElementById('notifList').innerHTML=d.map(n=>`<div class="notif"><b>${n.title}</b><p class="muted">${n.text}</p><small>${n.time}</small></div>`).join('')}
async function loadAcct(){let r=await fetch('/api/ad_accounts'); let d=await r.json(); document.getElementById('acctList').innerHTML=d.map(a=>`<div class="chip">🏦 ${a.name} - ${a.balance} ${a.currency} - ${a.status}</div>`).join('')}
async function loadAdmin(){let r=await fetch('/api/ads'); let d=await r.json(); document.getElementById('adminList').innerHTML=d.map(a=>`<div class="notif"><b>${a.name} - ${a.status}</b><p class="muted">الادمن: <button class="btn2" onclick="alert('تمت الموافقة ✅')">موافقة - Approve</button> <button class="btn2" onclick="alert('تم الرفض ❌')">رفض - Reject</button> <button class="btn2" onclick="alert('تم الايقاف ⏸️')">ايقاف - Pause</button></p></div>`).join('')||'لا توجد اعلانات معلقة'}
async function loadAds(){let r=await fetch('/api/ads'); let d=await r.json(); document.getElementById('adsList').innerHTML=d.map(a=>`<div class="chip">🖼️ ${a.name} - ${a.format} - ${a.status}</div>`).join('')||'لسه ما عملت اعلان'}
async function loadAnalytics(){let r=await fetch('/api/analytics'); let a=await r.json(); document.getElementById('aSpend').innerText=a.spend.toLocaleString(); document.getElementById('aReach').innerText=a.reach.toLocaleString(); document.getElementById('aLeads').innerText=a.leads; document.getElementById('aSales').innerText=a.sales; document.getElementById('aCalls').innerText=a.calls; document.getElementById('aQual').innerText=a.calls_qualified; document.getElementById('aLp').innerText=a.lp_views; document.getElementById('aRoas').innerText=a.roas+'x'; document.getElementById('aCpm').innerText=a.cpm; document.getElementById('aCpc').innerText=a.cpc; document.getElementById('aCtr').innerText=a.ctr; let cv=document.getElementById('chart'); let ctx=cv.getContext('2d'); ctx.strokeStyle='#FF4D8D'; ctx.lineWidth=3; ctx.beginPath(); [10,25,20,45,38,60,75,90].forEach((v,i)=>{let x=i*40+10,y=120-v; if(i==0) ctx.moveTo(x,y); else ctx.lineTo(x,y)}); ctx.stroke()}
loadAnalytics(); loadNotif();
</script></body></html>
"""
@app.get("/", response_class=HTMLResponse)
def home(): return HTML
@app.get("/api/analytics")
def ana(): return DB["analytics"]
@app.get("/api/notifications")
def notifs(): return DB["notifications"]
@app.get("/api/ad_accounts")
def accts(): return DB["ad_accounts"]
@app.get("/api/campaigns")
def list_c(): return DB["campaigns"]
@app.post("/api/campaigns")
def create_c(c: Campaign):
    d=c.dict(); d["id"]=str(uuid.uuid4())[:8]; d["created_at"]=str(datetime.datetime.now()); DB["campaigns"].append(d); return d
@app.post("/api/adsets")
def create_s(s: AdSet):
    d=s.dict(); d["id"]=str(uuid.uuid4())[:8]; DB["adsets"].append(d); return d
@app.get("/api/ads")
def list_ads(): return DB["ads"]
@app.post("/api/ads")
def create_ad(a: Ad):
    d=a.dict(); d["id"]=str(uuid.uuid4())[:8]; DB["ads"].append(d); return d
@app.post("/api/drafts")
def create_d(d: dict):
    d["id"]=str(uuid.uuid4())[:8]; DB["drafts"].append(d); return d
@app.get("/api/health")
def h(): return {"ok":True,"app":"NoorBook V33 PRO MAX"}
