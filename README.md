# پرسشنامه ارزیابی خطر بیماری قلبی-عروقی آترواسکلروتیک
## دانشگاه علوم پزشکی کرمانشاه

## فایل‌های مورد نیاز
app.py | model_xgb.pkl | feature_names.json | requirements.txt | README.md

## اجرای محلی
pip install -r requirements.txt
streamlit run app.py

## Streamlit Cloud
1. github.com → repository جدید: ascvd-app
2. همه ۵ فایل را آپلود کنید
3. share.streamlit.io → New app → ascvd-app → app.py → Deploy

## مشخصات مدل
XGBoost | ۱۰۰۰ نفر رجیستری قلب کرمانشاه
اعتبارسنجی: ۱۰-Fold × ۱۰ تکرار = ۱۰۰ ارزیابی
Accuracy: 91% | AUC: 0.971 | Sensitivity: 91% | Specificity: 91%

## سطوح خطر
کم‌خطر: احتمال کمتر از ۳۰٪
متوسط:  احتمال ۳۰٪ تا ۶۰٪
پرخطر:  احتمال بیشتر از ۶۰٪
