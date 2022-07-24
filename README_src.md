فولدر enums:
</br>
 در این فولدر یک فایل enums.py وجود دارد که در آن مقادیر static که در پروژه وجود دارد مقداردهی شده است.
 </br>
 </br>
فولدر requirments:
</br>
در این فولدر دو فایل numpy_encoder.py و news_dataset.py وجود دارد که در ادامه به شرح هر یک از آنها خواهیم پرداخت:
* فایل numpy_encoder.py برای save و load کردن numpy array می‌باشد.
* فایل news_dataset.py برای ساخت dataset از روی دیتا برای بخش transformer classification است
 
فایل‌های root اصلی فولدر src:
<ul dir="rtl">
  <li>

بخش preprocessing پروژه در فایل preprocessing.py وجود دارد بدین صورت که ابتدا دیتا crawl شده که در 
  <code>data/news.json</code>
است را لود می‌کنیم می‌کنیم و در ادامه دیتا را نرمالایز کرده سپس توکنایز می‌کنیم و سپس حرف‌های اضافه را حذف می‌کنیم و در نهایت lemmatize می‌کنیم و دیتا پیش‌پردازش شده را save می‌کنیم و در ادامه پروژه آن را
لود می‌کنیم. لازم به ذکر است که برای تحلیل لینک باید روی عنوان خبر‌ها پیش‌پردازش را انجام دهیم. بنابراین حالت دیگری برای پیش پردازش روی عنوان خبر را انجام می‌دهیم
همچنین نحوه دیتا پیش‌پردازش شده در حالت transformer classification متفاوت است که آن را با boolean متمایز می‌کنیم. همجنین برای transformer search از آنجا که
ترین کردن روی کل حجم دیتا بسیار زمان‌بر بود از 
  <code> data/news_12.json</code>
استفاده می‌کردیم که تنها روی ۱۲ صفحه از هر کتگوری کراول انجام می‌دهد. در نهایت فایل‌های save شده بدین صورت است که در 
  <code> models/preprocessed_data/data.plk</code>
دیتا کامل پیش‌پردازش شده روی متن می‌باشد، در
  <code>models/preprocessed_data/clf_data.plk‍‍</code>
دیتا کامل 
پیش‌پردازش شده روی متن برای transformer classification می‌باشد، در
  <code>models/preprocessed_data/tran_data.plk</code>
دیتا پیش پردازش شده روی متن که از هر کتگوری ۱۲ صفحه می‌باشد و در
  <code> models/preprocessed_data/title_data.plk</code>
دیتا کامل پیش پردازش شده بر روی عنوان خبر می‌باشد که برای تحلیل لینک کاربرد دارد. 
  </li>
  <li>
بخش query expansion پروژه در فایل query_expansion.py وجود دارد بدین 
  </li>
  <li>
    فایل boolean_search.py برای search کردن به روش بولین است. بد

  </li>
</ul>

 
