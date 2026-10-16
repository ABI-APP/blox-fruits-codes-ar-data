# blox-fruits-codes-ar-data

الترجمات العربية التي يحمّلها تطبيق **اكواد ماب blox fruits** (`com.abdullah.bloxfruits`) عن بُعد.

هذا المستودع خاص بالتطبيق العربي. بيانات اللعبة نفسها (الأكواد، الفواكه، الأدلة) تبقى في المستودع المشترك [`ABI-APP/fruit-codes-data`](https://github.com/ABI-APP/fruit-codes-data)، ولا يُعدَّل من هنا. هنا فقط **النص العربي** الذي يظهر بدل النص الإنجليزي.

## الملف `translations_ar.json`

```json
{
  "schema_version": 1,
  "updated_at": "2026-10-16",
  "translations": {
    "+10% Defense": "+10% دفاع",
    "Celestial Helmet pairs 10% all damage resistance with -5% all skill cooldown.": "يجمع Celestial Helmet بين …"
  }
}
```

- **المفتاح:** النص الإنجليزي **حرفيًا** كما يرد في بيانات اللعبة أو في كتالوج الإكسسوارات المضمّن في التطبيق، دون مسافات في أوله أو آخره. إذا تغيّر النص الإنجليزي ولو بحرف واحد، فهو مفتاح جديد.
- **القيمة:** الترجمة العربية، ويجب أن تحتوي حروفًا عربية.
- `schema_version` يجب أن يكون `1`.
- `updated_at` تاريخ بصيغة `YYYY-MM-DD`.
- الحدود: الملف 2 MB، و20,000 مدخل، و8,000 حرف للمفتاح أو للقيمة.

أكواد اللعبة والمعرّفات والأرقام والإحصاءات **لا تُترجم أبدًا**. التطبيق لا يمرّرها عبر هذا الملف.

## ترتيب الأولوية في التطبيق

1. ترجمة صالحة من هذا الملف (آخر نسخة نجح التحقق منها).
2. الكتالوج العربي المضمّن داخل التطبيق.
3. النص الأصلي. يظهر معه تنبيه «لم تُراجع ترجمته العربية بعد».

## طريقة التحديث

1. عدّل `translations_ar.json`: أضف مفتاحًا جديدًا، أو صحّح قيمة موجودة.
2. تحقّق محليًا:
   ```
   python tools/validate_translations.py
   ```
3. أنشئ commit وارفعه إلى الفرع `main`، ثم انتظر نجاح فحص **Validate translations** في GitHub Actions.
4. يصل التحديث إلى المستخدمين تلقائيًا، دون إصدار AAB جديد:
   - يفحص التطبيق الملف عند التشغيل، بحد أقصى مرة كل 6 ساعات بعد آخر تحميل ناجح، ومرة كل 30 دقيقة بعد محاولة فاشلة.
   - رابط `raw.githubusercontent.com` قد يُخزَّن مؤقتًا لبضع دقائق.
   - النص الجديد يظهر في الشاشات التي تُفتح بعد التحميل، وفي كل الشاشات عند التشغيل التالي.

## الأمان والعمل دون اتصال

- يحفظ التطبيق آخر ملف صالح محليًا، ويعمل به دون اتصال.
- أي ملف JSON تالف، أو برقم `schema_version` غير مدعوم، أو بلا أي مدخل صالح، يُرفض بالكامل، وتبقى النسخة المحفوظة.
- المدخل المعطوب وحده يتجاهله التطبيق، لكن فحص GitHub Actions يرفضه، فلا يصل إلى المستخدمين.
- لا تضع في هذا المستودع أي مفاتيح أو كلمات مرور أو إعدادات توقيع. فهو **عام**.

## الإنشاء الأولي

النسخة الأولى صُدّرت من الكتالوج العربي المراجَع داخل التطبيق، عبر `tool/export_translations.dart` في مستودع التطبيق، دون إعادة ترجمة (935 نصًا).

---

*English summary:* public Arabic translation overlay for the Arabic Blox Fruits codes app. Keys are exact English source strings; values are Arabic. Edit `translations_ar.json`, run `python tools/validate_translations.py`, push to `main`. The app applies valid remote entries over its bundled catalog, caches the last valid file for offline use, and rejects invalid documents without discarding the cached copy.
