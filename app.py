import streamlit as st
import joblib, json, os, pandas as pd

st.set_page_config(
    page_title="پرسشنامه ارزیابی خطر بیماری قلبی-عروقی",
    page_icon="❤️",
    layout="centered"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;600;700&display=swap');
*{font-family:'Vazirmatn',Tahoma,sans-serif!important}
html,body,.stApp,.block-container,[class*="css"]{direction:rtl!important;text-align:right!important}
.stRadio [role="radiogroup"]{flex-direction:row-reverse!important;justify-content:flex-end!important}
.stRadio [role="radiogroup"] label{direction:rtl!important}
label,.stSelectbox label,.stRadio label,.stNumberInput label{direction:rtl!important;text-align:right!important}
.block-container{padding-top:.8rem!important;max-width:780px!important}
[data-testid="column"]{direction:rtl!important}

.hdr{
    background:linear-gradient(135deg,#1a3a5c,#2563a8);
    color:#fff;border-radius:12px;
    padding:1.2rem 1.4rem;text-align:center;margin-bottom:1rem;
}
.hdr h1{font-size:1.15rem;margin:0;line-height:1.5;font-weight:700}
.hdr p{font-size:.78rem;opacity:.8;margin-top:4px}

.sec{background:#1a3a5c;color:#fff;border-radius:8px;
    padding:.45rem .9rem;font-weight:700;margin:1.1rem 0 .7rem;
    font-size:.9rem;text-align:right}

.note{background:#f0f9ff;border:1px solid #bae6fd;border-radius:8px;
    padding:.65rem .9rem;font-size:.79rem;color:#0369a1;
    margin:.5rem 0;line-height:1.9;text-align:right;direction:rtl}

.sub{color:#2563a8;font-weight:700;font-size:.85rem;
    margin:.7rem 0 .25rem;text-align:right;direction:rtl}

/* نتایج */
.result-high{background:#fff0f0;border:3px solid #e63946;
    border-radius:12px;padding:1.4rem;text-align:center}
.result-mid{background:#fffbeb;border:3px solid #f59e0b;
    border-radius:12px;padding:1.4rem;text-align:center}
.result-low{background:#f0faf9;border:3px solid #1baf7a;
    border-radius:12px;padding:1.4rem;text-align:center}

.warn{background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;
    padding:.7rem;font-size:.77rem;color:#64748b;
    margin-top:.8rem;line-height:1.7;text-align:right;direction:rtl}
</style>""", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    base = os.path.dirname(os.path.abspath(__file__))
    m = joblib.load(os.path.join(base, "model_xgb.pkl"))
    with open(os.path.join(base, "feature_names.json"), encoding="utf-8") as f:
        ft = json.load(f)
    return m, ft

model, FEATURES = load_model()

# ── هدر بدون آیکون قلب ───────────────────────────────────────────────────────
st.markdown("""<div class="hdr">
<h1>پرسشنامه ارزیابی خطر بیماری قلبی‌عروقی آترواسکلروتیک</h1>
<p>رجیستری قلب کرمانشاه — دانشگاه علوم پزشکی کرمانشاه</p>
</div>""", unsafe_allow_html=True)

# ═══ بخش ۱: اطلاعات فردی ════════════════════════════════════════════════════
st.markdown('<div class="sec">👤 اطلاعات فردی و اجتماعی</div>', unsafe_allow_html=True)

edu_map = {
    "بی‌سواد":1,
    "ابتدایی (۱ تا ۵ کلاس)":2,
    "زیر دیپلم (۶ تا ۱۱ کلاس)":3,
    "دیپلم":4,
    "فوق دیپلم":5,
    "لیسانس":6,
    "فوق لیسانس":7,
    "دکترا (PhD / MD / ...)":8
}
education_level = edu_map[st.selectbox("وضعیت سواد:", list(edu_map.keys()), index=3)]

mar_map = {"مجرد":1, "متأهل":2, "مطلقه":3, "همسر فوت شده":4}
marital_status = mar_map[st.selectbox("وضعیت تأهل فعلی:", list(mar_map.keys()), index=1)]

family_member = st.number_input(
    "تعداد اعضای خانوار (زیر یک سقف و سر یک سفره):",
    min_value=1, max_value=20, value=3, step=1)

inc_map = {"خیلی پایین":1, "پایین":2, "متوسط":3, "بالا":4, "خیلی بالا":5}
incomeself_ranking = inc_map[st.selectbox(
    "رتبه‌بندی درآمد خانوار از نظر خودتان:", list(inc_map.keys()), index=1)]

# ═══ بخش ۲: دخانیات ══════════════════════════════════════════════════════════
st.markdown('<div class="sec">🚬 مصرف دخانیات و مواد</div>', unsafe_allow_html=True)

def yes_no(label, key):
    v = st.radio(label, ["خیر", "بله"], index=0, key=key, horizontal=True)
    return 1 if v == "بله" else 0

cigarette = yes_no("۵) آیا تا کنون به طور روزانه یا هفتگی حداقل ۶ ماه سیگار کشیده‌اید؟", "cig")
if cigarette:
    st.markdown('<div class="sub">جزئیات مصرف سیگار:</div>', unsafe_allow_html=True)
    c1,c2,c3 = st.columns(3)
    with c1: st.number_input("مدت مصرف (سال):", 0,70,5, key="cig_yr")
    with c2: st.number_input("متوسط نخ در روز:", 1,100,10, key="cig_nd")
    with c3: st.radio("آخرین بار مصرف:", ["سال جاری","سال‌های قبل"], key="cig_l", horizontal=True)

pipe_used = yes_no("۷) آیا تا کنون پیپ به طور روزانه یا هفتگی حداقل ۶ ماه کشیده‌اید؟", "pipe")
if pipe_used:
    st.markdown('<div class="sub">جزئیات مصرف پیپ:</div>', unsafe_allow_html=True)
    c1,c2,c3 = st.columns(3)
    with c1: st.number_input("مدت مصرف (سال):", 0,70,3, key="pipe_yr")
    with c2: st.number_input("دفعات در روز:", 1,20,1, key="pipe_nd")
    with c3: st.radio("آخرین بار مصرف:", ["سال جاری","سال‌های قبل"], key="pipe_l", horizontal=True)

waterpipe = yes_no("۸) آیا تا کنون قلیان به طور روزانه یا هفتگی حداقل ۶ ماه کشیده‌اید؟", "hook")
if waterpipe:
    st.markdown('<div class="sub">جزئیات مصرف قلیان:</div>', unsafe_allow_html=True)
    c1,c2,c3 = st.columns(3)
    with c1: st.number_input("مدت مصرف (سال):", 0,70,2, key="hook_yr")
    with c2: st.number_input("دفعات در روز:", 1,10,1, key="hook_nd")
    with c3: st.radio("آخرین بار مصرف:", ["سال جاری","سال‌های قبل"], key="hook_l", horizontal=True)

opium_used = yes_no("۹) آیا تا کنون تریاک/شیره/سوخته/هرویین حداقل ۶ ماه مصرف کرده‌اید؟", "opium")
if opium_used:
    st.markdown('<div class="sub">جزئیات مصرف تریاک:</div>', unsafe_allow_html=True)
    c1,c2,c3,c4 = st.columns(4)
    with c1: st.radio("نوع:", ["خوراکی","دود","تزریق"], key="opium_t", horizontal=True)
    with c2: st.number_input("مدت (سال):", 0,70,3, key="opium_yr")
    with c3: st.number_input("دفعات/هفته:", 1,21,3, key="opium_wk")
    with c4: st.radio("آخرین بار:", ["سال جاری","سال‌های قبل"], key="opium_l", horizontal=True)

methadone_used = yes_no("۱۰) آیا تا کنون متادون/اپیوییدهای درمانی حداقل ۶ ماه مصرف کرده‌اید؟", "meth")
if methadone_used:
    c1,c2 = st.columns(2)
    with c1: st.number_input("مدت مصرف (سال):", 0,70,2, key="meth_yr")
    with c2: st.radio("آخرین بار:", ["سال جاری","سال‌های قبل"], key="meth_l", horizontal=True)

other_drug_abuse = yes_no("۱۱) آیا تا کنون سوءمصرف سایر مواد حداقل ۶ ماه داشته‌اید؟", "odrug")
if other_drug_abuse:
    c1,c2,c3 = st.columns(3)
    with c1: st.text_input("نوع ماده:", key="odrug_t")
    with c2: st.number_input("مدت (سال):", 0,70,2, key="odrug_yr")
    with c3: st.number_input("دفعات/هفته:", 1,21,3, key="odrug_wk")

alcohol_used = yes_no("۱۲) آیا تا کنون مشروبات الکلی به طور هفتگی حداقل ۶ ماه مصرف کرده‌اید؟", "alc")
if alcohol_used:
    c1,c2 = st.columns(2)
    with c1: st.number_input("مدت مصرف (سال):", 0,70,2, key="alc_yr")
    with c2: st.radio("آخرین بار:", ["سال جاری","سال‌های قبل"], key="alc_l", horizontal=True)

# ═══ بخش ۳: سابقه پزشکی ═════════════════════════════════════════════════════
st.markdown('<div class="sec">🏥 سابقه پزشکی</div>', unsafe_allow_html=True)

def disease_q(label, key):
    # ✅ مقایسه دقیق == چون "ندارد" شامل "دارد" است
    v = st.radio(label, ["ندارد", "دارد", "نامشخص"], index=0, key=key, horizontal=True)
    return 1 if v == "دارد" else 0

diabetes     = disease_q("۱۳) دیابت (بر اساس تشخیص پزشک):", "diab")
if diabetes:
    st.number_input("مدت ابتلا از زمان تشخیص (سال):", 0,60,5, key="diab_yr")

hypertension = disease_q("۱۴) پرفشاری خون (بر اساس تشخیص پزشک):", "htn")
if hypertension:
    st.number_input("مدت ابتلا از زمان تشخیص (سال):", 0,60,5, key="htn_yr")

Dyslipidemia = disease_q("۱۵) اختلال چربی خون — هیپرلیپیدمی (بر اساس تشخیص پزشک):", "hlip")
if Dyslipidemia:
    st.number_input("مدت ابتلا از زمان تشخیص (سال):", 0,60,5, key="hlip_yr")

family_history_coronary = disease_q("۱۶) سابقه خانوادگی بیماری کرونر زودرس:", "fhx")

# ═══ بخش ۴: تن‌سنجی ═════════════════════════════════════════════════════════
st.markdown('<div class="sec">📏 اندازه‌گیری‌های تن‌سنجی</div>', unsafe_allow_html=True)
c1,c2 = st.columns(2)
with c1: height = st.number_input("۱۷) قد (سانتی‌متر):", 100, 220, 168)
with c2: weight = st.number_input("۱۸) وزن (کیلوگرم):", 30, 300, 70)
BMI = weight / ((height/100)**2)
st.metric("شاخص توده بدنی (BMI) — خودکار محاسبه شد:", f"{BMI:.1f} kg/m²")

# ═══ بخش ۵: تغذیه ════════════════════════════════════════════════════════════
st.markdown('<div class="sec">🥗 تغذیه (متوسط طی یک سال اخیر)</div>', unsafe_allow_html=True)

st.markdown("""<div class="note">
<b>یک واحد میوه</b> معادل: یک عدد سیب/پرتقال/هلو/لیموشیرین متوسط، دو نارنگی یا کیوی،
سه انجیر تازه یا زردآلو، نصف موز بزرگ، ۱.۲۵ لیوان توت‌فرنگی،
۱۲ گیلاس، یک لیوان آلبالو، ۱.۵ لیوان هندوانه/خربزه/طالبی قاچ‌شده.<br>
<b>یک واحد سبزی</b> معادل: یک لیوان سبزی برگ‌دار خام (اسفناج، کاهو، سبزی خوردن)،
نصف لیوان سبزی پخته یا خردشده، نصف لیوان نخود/لوبیا سبز/هویج خردشده،
یک عدد گوجه‌فرنگی، هویج، خیار، پیاز یا سیب‌زمینی متوسط.
</div>""", unsafe_allow_html=True)

st.markdown('<div class="sub">۲۱) مصرف سبزیجات:</div>', unsafe_allow_html=True)
c1,c2 = st.columns(2)
with c1: vegetables_freq = st.number_input("بار در هفته:", 0,21,3, step=1, key="veg_f")
with c2: st.number_input("هر بار چند واحد:", 1,10,2, step=1, key="veg_u")

st.markdown('<div class="sub">۲۲) مصرف میوه:</div>', unsafe_allow_html=True)
c1,c2 = st.columns(2)
with c1: fruits_freq = st.number_input("بار در هفته:", 0,28,5, step=1, key="fr_f")
with c2: st.number_input("هر بار چند واحد:", 1,10,2, step=1, key="fr_u")

salt_map = {"نسبتاً کم":1, "متوسط":2, "نسبتاً زیاد":3}
salt = salt_map[st.radio(
    "۲۳) استفاده از نمکدان / خیارشور / مواد پرنمک:",
    list(salt_map.keys()), index=0, horizontal=True)]

c1,c2 = st.columns(2)
with c1:
    sweet_drinks = st.number_input(
        "۲۴) نوشیدنی صنعتی (نوشابه، ماءالشعیر، آب‌میوه صنعتی — به جز دوغ) — بار/هفته:",
        0,21,1, step=1)
with c2:
    pastry_bread = st.number_input(
        "۲۵) نان روغنی / شیرینی / کیک / بیسکویت — بار/هفته:",
        0,28,1, step=1)

# ═══ بخش ۶: فعالیت بدنی ═════════════════════════════════════════════════════
st.markdown('<div class="sec">🏃 فعالیت بدنی (متوسط طی یک سال اخیر)</div>', unsafe_allow_html=True)
st.markdown("""<div class="note">
اگر در حین فعالیت قادر به حرف زدن هستید → <b>متوسط</b> |
اگر پس از چند کلمه نیاز به توقف و نفس دارید → <b>شدید</b>
</div>""", unsafe_allow_html=True)

st.markdown('<div class="sub">۲۶) فعالیت فیزیکی هنگام کار:</div>', unsafe_allow_html=True)
c1,c2,c3,c4 = st.columns(4)
with c1: work_heavy_freq    = st.number_input("فعالیت شدید (بار/هفته):",   0,14,0, step=1, key="wh_f")
with c2: st.number_input("هر بار (دقیقه):", 0,480,30, step=10, key="wh_m")
with c3: work_moderate_freq = st.number_input("فعالیت متوسط (بار/هفته):", 0,14,0, step=1, key="wm_f")
with c4: st.number_input("هر بار (دقیقه):", 0,480,30, step=10, key="wm_m")

st.markdown('<div class="sub">۲۷) فعالیت هنگام رفت‌وآمد (پیاده‌روی یا دوچرخه‌سواری):</div>', unsafe_allow_html=True)
c1,c2 = st.columns(2)
with c1: commute_freq = st.number_input("بار در هفته:", 0,14,0, step=1, key="cm_f")
with c2: st.number_input("هر بار (دقیقه):", 0,480,30, step=10, key="cm_m")

st.markdown('<div class="sub">۲۸) فعالیت هنگام اوقات فراغت:</div>', unsafe_allow_html=True)
c1,c2,c3,c4 = st.columns(4)
with c1: leisure_heavy_freq    = st.number_input("فعالیت شدید (بار/هفته):",   0,14,0, step=1, key="lh_f")
with c2: st.number_input("هر بار (دقیقه):", 0,480,30, step=10, key="lh_m")
with c3: leisure_moderate_freq = st.number_input("فعالیت متوسط (بار/هفته):", 0,14,0, step=1, key="lm_f")
with c4: st.number_input("هر بار (دقیقه):", 0,480,30, step=10, key="lm_m")

c1,c2 = st.columns(2)
with c1:
    inactive_time = st.number_input(
        "۲۹) ساعات بی‌تحرکی روزانه (نشستن، تلویزیون...) — ساعت:",
        0, 24, 4, step=1)
with c2:
    sleep_hours = st.number_input(
        "۳۰) ساعات خواب در شبانه‌روز — ساعت:",
        2, 14, 7, step=1)

stress_map = {"خیلی کم":1, "کم":2, "متوسط":3, "زیاد":4, "خیلی زیاد":5}
stress_level = stress_map[st.radio(
    "۳۱) طی یک سال گذشته چه مقدار تحت فشار روحی-روانی بوده‌اید؟",
    list(stress_map.keys()), index=2, horizontal=True)]

# ═══ دکمه پیش‌بینی ══════════════════════════════════════════════════════════
st.markdown("---")
if st.button("🔍  دریافت نتیجه ارزیابی", use_container_width=True, type="primary"):

    inp = {
        "education_level":         float(education_level),
        "marital_status":          float(marital_status),
        "family_member":           float(family_member),
        "incomeself_ranking":      float(incomeself_ranking),
        "cigarette":               float(cigarette),
        "pipe_used":               float(pipe_used),
        "waterpipe":               float(waterpipe),
        "opium_used":              float(opium_used),
        "methadone_used":          float(methadone_used),
        "other_drug_abuse":        float(other_drug_abuse),
        "alcohol_used":            float(alcohol_used),
        "diabetes":                float(diabetes),
        "hypertension":            float(hypertension),
        "Dyslipidemia":            float(Dyslipidemia),
        "family_history_coronary": float(family_history_coronary),
        "vegetables_freq":         float(vegetables_freq),
        "fruits_freq":             float(fruits_freq),
        "salt":                    float(salt),
        "sweet_drinks":            float(sweet_drinks),
        "pastry_bread":            float(pastry_bread),
        "work_heavy_freq":         float(work_heavy_freq),
        "work_moderate_freq":      float(work_moderate_freq),
        "commute_freq":            float(commute_freq),
        "leisure_heavy_freq":      float(leisure_heavy_freq),
        "leisure_moderate_freq":   float(leisure_moderate_freq),
        "inactive_time":           float(inactive_time),
        "sleep_hours":             float(sleep_hours),
        "stress_level":            float(stress_level),
        "BMI":                     float(BMI),
    }

    X = pd.DataFrame([inp])[FEATURES]
    proba    = model.predict_proba(X)[0]
    prob_sick    = float(proba[1])   # احتمال بیمار
    prob_healthy = float(proba[0])   # احتمال سالم
    pct_s = round(prob_sick * 100, 1)
    pct_h = round(prob_healthy * 100, 1)

    # ── سه سطح خطر بر اساس توزیع واقعی داده ──────────────────────────────────
    # < 30% = کم‌خطر | 30-60% = متوسط | > 60% = پرخطر
    if prob_sick >= 0.60:
        risk_level = "high"
        risk_label = "پرخطر — در معرض بیماری قلبی‌عروقی آترواسکلروتیک"
        risk_icon  = "🔴"
        risk_color = "#e63946"
        css_class  = "result-high"
        advice     = "مراجعه فوری به پزشک متخصص قلب توصیه می‌شود."
    elif prob_sick >= 0.30:
        risk_level = "mid"
        risk_label = "خطر متوسط — نیاز به بررسی بیشتر"
        risk_icon  = "🟡"
        risk_color = "#d97706"
        css_class  = "result-mid"
        advice     = "مراجعه به پزشک و اصلاح سبک زندگی توصیه می‌شود."
    else:
        risk_level = "low"
        risk_label = "کم‌خطر — وضعیت مطلوب"
        risk_icon  = "🟢"
        risk_color = "#1baf7a"
        css_class  = "result-low"
        advice     = "ادامه سبک زندگی سالم و پایش منظم توصیه می‌شود."

    st.markdown("---")
    st.markdown("## 📊 نتیجه ارزیابی")

    st.markdown(f"""<div class="{css_class}">
    <div style="font-size:2.5rem;margin-bottom:.3rem">{risk_icon}</div>
    <h2 style="color:{risk_color};margin:.2rem 0;font-size:1.3rem">{risk_label}</h2>
    <p style="color:#555;margin:.4rem 0;font-size:.95rem">
        احتمال بیماری: <b style="font-size:1.6rem;color:{risk_color}">{pct_s}٪</b>
        &nbsp;|&nbsp;
        احتمال سلامت: <b style="color:#555">{pct_h}٪</b>
    </p>
    <p style="font-size:.82rem;color:#666;margin-top:.4rem">{advice}</p>
    </div>""", unsafe_allow_html=True)

    # نوار احتمال
    st.progress(prob_sick, text=f"احتمال بیماری: {pct_s}٪")

    # راهنمای سطوح
    st.markdown("""
    <div style="display:flex;gap:1rem;margin:.6rem 0;flex-direction:row-reverse;font-size:.78rem">
        <span>🟢 کم‌خطر: کمتر از ۳۰٪</span>
        <span>🟡 متوسط: ۳۰٪ تا ۶۰٪</span>
        <span>🔴 پرخطر: بیشتر از ۶۰٪</span>
    </div>
    """, unsafe_allow_html=True)

    # عوامل خطر و محافظتی
    c1,c2 = st.columns(2)
    with c1:
        risks = []
        if inactive_time > 4:             risks.append("بی‌تحرکی روزانه بالا")
        if work_moderate_freq < 2 and commute_freq < 2: risks.append("فعالیت فیزیکی کم")
        if opium_used == 1:               risks.append("مصرف تریاک/مواد مخدر")
        if cigarette == 1:                risks.append("مصرف سیگار")
        if waterpipe == 1:                risks.append("مصرف قلیان")
        if hypertension == 1:             risks.append("پرفشاری خون")
        if diabetes == 1:                 risks.append("دیابت")
        if family_history_coronary == 1:  risks.append("سابقه خانوادگی کرونر")
        if education_level <= 2:          risks.append("تحصیلات پایین")
        if BMI > 30:                      risks.append(f"اضافه وزن (BMI={BMI:.1f})")
        if stress_level >= 4:             risks.append("استرس بالا")
        if salt == 3:                     risks.append("مصرف زیاد نمک")
        if risks:
            st.markdown("**⚠️ عوامل خطر شناسایی‌شده:**")
            for r in risks: st.markdown(f"- {r}")

    with c2:
        prot = []
        if work_moderate_freq >= 4:       prot.append("فعالیت شغلی منظم")
        if commute_freq >= 3:             prot.append("پیاده‌روی رفت‌وآمد")
        if vegetables_freq >= 5:          prot.append("مصرف کافی سبزیجات")
        if fruits_freq >= 5:              prot.append("مصرف کافی میوه")
        if inactive_time <= 2:            prot.append("سبک زندگی فعال")
        if sleep_hours >= 7:              prot.append("خواب کافی")
        if BMI <= 25:                     prot.append(f"وزن مناسب (BMI={BMI:.1f})")
        if prot:
            st.markdown("**✅ عوامل محافظتی:**")
            for p in prot: st.markdown(f"- {p}")

    # مشخصات مدل
    with st.expander("📊 مشخصات مدل"):
        c1,c2,c3,c4 = st.columns(4)
        c1.metric("Accuracy",    "91.0%")
        c2.metric("AUC",         "0.971")
        c3.metric("Sensitivity", "91.0%")
        c4.metric("Specificity", "91.0%")
        st.caption(
            "XGBoost | ۱۰۰۰ نفر رجیستری قلب کرمانشاه | "
            "۱۰-Fold × ۱۰ تکرار = ۱۰۰ ارزیابی مستقل | "
            "AUC در همه ارزیابی‌ها: ۰.۹۳ تا ۱.۰"
        )

    st.markdown("""<div class="warn">
    این سیستم صرفاً جهت پژوهش و غربالگری اولیه طراحی شده است.
    نتیجه ارزیابی جایگزین تشخیص پزشکی نمی‌باشد.
    در صورت نیاز با پزشک متخصص مشورت کنید.
    </div>""", unsafe_allow_html=True)

st.caption("دانشگاه علوم پزشکی کرمانشاه · رجیستری قلب کرمانشاه")
