





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
 </br>
  <li>
بخش query expansion پروژه در فایل query_expansion.py وجود دارد بدین صورت است که کوئری را می‌گیرد و با دو روش آن را گسترش می‌دهد. روش اول استفاده از الگوریتم rocchio است بدین صورت که امبدینگ هر کوئری را محاسبه می‌کنیم و با میانگین امبدینگ ده تا مرتبط‌ترین داک جمع می‌کنیم و از میانگین امبدینگ ده تا نامرتبط‌ترین داک‌ها کم می‌کنیم و حال امبدینگ حاصل را به عنوان کوئری جدید می‌گیریم و آن را جستجو می‌کنیم. (از این روش برای گسترش کوئری در روش‌هاس جست‌وجو transformers و fasttext استفاده می‌کنیم.) روش دیگری که پیاده‌سازی کرده‌ایم بدین صورت است که ابتدا برای تمام کلمات تمام داک‌هایمان امبدینگ fasttext آن را محاسبه کرده و در 
   <code>models/QE_fasttext/all_words_vectors_emb_fasttext.json</code>
   ذخیره می‌کنیم و حال برای تک تک کلمات کوئری‌مان امبدینگ fastetxt محاسبه می‌کنیم و فاصله کسینوسی تک تک کلمات کوئری‌مان را با امبدینگ fasttext ای که برای تمام کلمات تمام داک‌هایمان به دست آورده بودیم محاسبه می‌کنیم. (یک threshold برای فاصله کسینوسی برای جلوگیری از شباهت بسیار زیاد و بیهوده بودن گسترش کوئری‌مان در نظر می‌گیریم.) در نهایت کوئری‌مان را با کلمات به دست آمده جایگزین می‌کنیم و کوئری جدیدمان را جستجو می‌کنیم.
</br>
   ارزیابی query expansion با معیار MRR را در این 
  <a href="">لینک</a>
   می توانید مشاهده کنید.
  </li>
  </br>
  <li>
 فایل boolean_search.py برای search کردن به روش بولین است. بدبن گونه عمل می کنیم که با کلمات کوئری‌مان و تمام داک‌هایمان یک ماتریس sparse می‌سازیم و در نهایت خبرهایی را به کاربر نشان می‌دهیم که تمام کلمات کوئری‌مان در متن خبر آمده باشد.
</br>
 ارزیابی boolean search با معیار MRR را در این 
  <a href="https://docs.google.com/spreadsheets/d/13742g0HNDlRK0NYwLdljk8krcd-qf9AprE-cyuszTaQ/edit#gid=0">لینک</a>
   می توانید مشاهده کنید.
  </li>
  </br>
  <li>
 فایل tfidf_search.py برای search کردن به روش tfidf است. بدین گونه عمل می‌کنیم که مدل tfidf vectorizer را در 
 <code>models/tfidf_search/tfidf.pk</code>
 ذخیره می‌کنیم. همچنین ماتریس sparse به دست آمده از tfidf را نیز در 
 <code>models/tfidf_search/tfidf_tran.npz</code>
 ذخیره می‌کنیم حال کوئری داده شده را با tfidf vectorizer به وکتور تبدیل می‌کنیم و فاصله کسینوسی میان وکتور کوئری و وکتور‌های داک محاسبه می‌کنیم و با محاسبه فاصله کسینوسی نزدیک‌ترین خبر‌ها را خروجی می‌دهیم. 
</br>
 ارزیابی tfidf search با معیار MRR را در این 
  <a href="https://docs.google.com/spreadsheets/d/13742g0HNDlRK0NYwLdljk8krcd-qf9AprE-cyuszTaQ/edit#gid=324656315">لینک</a>
   می توانید مشاهده کنید.
  </li>
  </br> 
  <li>
 فایل transformer_search.py برای search کردن به روش transformer است. بدین گونه عمل می‌کنیم که از مدل pars big bert که روی زبان فارسی train شده است استفاده می‌کنیم و با استفاده از tokenizer این کتابخانه دیتامان را توکنایز می‌کنیم و آن را روی دیتا خودمان fine tune می‌کنیم و مدلمان را در 
 <code>models/transformers_search/transformer_model.model</code>
 ذخیره کرده و توکنایزرمان را نیز در
 <code>models/transformers_search/transformer_tokenizer</code>
 ذخیره می‌کنیم. حال برای هر داک میانگین امبدینگ توکنایز شده آن را به عنوان امبدینگ داک در نظر می‌گیریم و آن را در 
 <code>models/transformers_search/transformer_vectors_emb.json</code>
 ذخیره می‌کنیم. همچنین کوئری‌مان را نیز توکنایز می‌کنیم و امبدینگ آن را نیز با استفاده از مدل‌مان محاسبه می‌کنیم و در نهایت با محاسبه فاصله کوسینوسی مرتبط‌ترین داک‌های آن را به عنوان خروجی می‌دهیم.
 ارزیابی tfidf search با معیار MRR را در این 
  <a href="https://docs.google.com/spreadsheets/d/13742g0HNDlRK0NYwLdljk8krcd-qf9AprE-cyuszTaQ/edit#gid=109295346">لینک</a>
   می توانید مشاهده کنید.

 </li>
 </br>
 <li>
 فایل boolean_search.py برای search کردن به روش boolean است. بدین گونه عمل می‌کنیم که از مدل fasttext استفاده می‌کنیم و آن را روی دیتا خودمان ترین می‌کنیم. سپس آن را در 
 <code>models/fasttext_search/fasttext.bin</code>
 ذخیره می‌کنیم و میانیگین امبدینگ‌های کلمات داک‌مان را محاسبه می‌کنیم و در 
 <code>models/fasttext_search/fasttext_vectors_emb.json</code>
 ذخیره می‌کنیم سپس امبدینگ کوئری‌مان را محاسبه کرده و در نهایت با محاسبه فاصله کوسینوسی مرتبط‌ترین داک‌های آن را به عنوان خروجی می‌دهیم.
 ارزیابی tfidf search با معیار MRR را در این 
  <a href="https://docs.google.com/spreadsheets/d/13742g0HNDlRK0NYwLdljk8krcd-qf9AprE-cyuszTaQ/edit#gid=170900943">لینک</a>
   می توانید مشاهده کنید
 </li>
</li>
</ul>

 
