# دليل المستخدم / User Guide

## BLK-REV Extractor Pro v1.0

---

## فهرس المحتويات / Table of Contents

1. [مقدمة / Introduction](#مقدمة--introduction)
2. [التثبيت / Installation](#التثبيت--installation)
3. [بدء الاستخدام / Getting Started](#بدء-الاستخدام--getting-started)
4. [الواجهة الرسومية / GUI Usage](#الواجهة-الرسومية--gui-usage)
5. [سطر الأوامر / CLI Usage](#سطر-الأوامر--cli-usage)
6. [توليد المفاتيح / Key Generation](#توليد-المفاتيح--key-generation)
7. [استكشاف الأخطاء / Troubleshooting](#استكشاف-الأخطاء--troubleshooting)

---

## مقدمة / Introduction

### ما هو BLK-REV Extractor؟

**BLK-REV Extractor Pro** هو أداة متخصصة لاستخراج وتحليل البيانات من ملفات **BLK .DAT** و **REV .DAT** المستخدمة في أنظمة معينة خلال الفترة **2009-2014**.

### المميزات الرئيسية

- ✅ دعم جميع إصدارات 2009-2014
- ✅ فك تشفير متعدد الخوارزميات (XOR, AES)
- ✅ فك ضغط متعدد الصيغ (zlib, LZ4, Zstandard)
- ✅ تصدير إلى CSV, Excel, JSON, XML
- ✅ واجهة عربية/إنجليزية
- ✅ CLI + GUI

---

## التثبيت / Installation

### المتطلبات

- Python 3.8 أو أحدث
- Windows 7/8/10/11 أو Linux أو macOS

### خطوات التثبيت

```bash
# 1. استنساخ المستودع
git clone https://github.com/yourusername/blk-rev-extractor.git
cd blk-rev-extractor

# 2. إنشاء بيئة افتراضية (موصى به)
python -m venv venv

# 3. تفعيل البيئة
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# 4. تثبيت المتطلبات
pip install -r requirements.txt

# 5. تشغيل الاختبارات
python test_sample.py
```

---

## بدء الاستخدام / Getting Started

### الوضع التفاعلي (GUI)

```bash
python main.py
```

### سطر الأوامر (CLI)

```bash
# استخراج البيانات
python cli.py extract -i file.blk -o output.json -f json

# توليد مفاتيح
python cli.py keys --all -o keys.json

# معلومات الملف
python cli.py info -i file.rev
```

---

## الواجهة الرسومية / GUI Usage

### 1. فتح ملف

1. انقر على **"فتح ملف"** أو استخدم القائمة
2. اختر ملف `.blk` أو `.rev` أو `.dat`
3. سيتم عرض معلومات الملف تلقائياً

### 2. توليد المفاتيح

1. اذهب إلى **"أدوات > مولد المفاتيح"**
2. اختر السنة المناسبة (2009-2014)
3. انقر **"توليد"**
4. احفظ المفاتيح في ملف

### 3. استخراج البيانات

1. بعد تحميل الملف، انقر **"استخراج البيانات"**
2. انتظر حتى اكتمال العملية
3. راجع النتائج في علامات التبويب

### 4. التصدير

1. اذهب إلى **"تصدير"**
2. اختر الصيغة (CSV, Excel, JSON)
3. حدد المسار
4. انقر **"تصدير"**

---

## سطر الأوامر / CLI Usage

### الأوامر المتاحة

| الأمر | الوصف |
|-------|-------|
| `extract` | استخراج البيانات من ملف |
| `keys` | توليد مفاتيح التشفير |
| `info` | عرض معلومات الملف |

### أمثلة

#### استخراج بيانات

```bash
# استخدام مفتاح محدد
python cli.py extract -i data.blk -o output.csv -f csv -k "a1b2c3..."

# توليد مفتاح تلقائياً للسنة 2012
python cli.py extract -i data.blk -o output.json -f json -y 2012
```

#### توليد مفاتيح

```bash
# مفتاح لسنة واحدة
python cli.py keys -y 2010 -o key_2010.json

# جميع السنوات
python cli.py keys --all -o all_keys.json
```

---

## توليد المفاتيح / Key Generation

### أنواع المفاتيح حسب السنة

| السنة | الخوارزمية | الحجم | الاستخدام |
|-------|-----------|-------|-----------|
| 2009 | XOR | 1 بايت | تشفير بسيط |
| 2010 | AES-128-CBC | 16 بايت | تشفير قياسي |
| 2011 | AES-256-CBC | 32 بايت | تشفير قوي |
| 2012 | AES-256-CBC | 32 بايت | تشفير قوي |
| 2013 | AES-256-GCM | 32 بايت | تشفير مصادق |
| 2014 | AES-256-GCM | 32 بايت | تشفير مصادق |

### طريقة التوليد

تستخدم الأداة **PBKDF2-HMAC-SHA256** لتوليد المفاتيح:

```
Key = PBKDF2(Password, Salt, Iterations, KeySize)
```

حيث:
- **Password**: عبارة سرية فريدة لكل سنة
- **Salt**: قيمة ثابتة خاصة بكل سنة
- **Iterations**: عدد دورات التجزئة (1000-25000)
- **KeySize**: حجم المفتاح المطلوب

---

## استكشاف الأخطاء / Troubleshooting

### المشكلة: فشل تحميل الملف

**الحل:**
- تأكد من أن الملف غير تالف
- تحقق من امتداد الملف (.blk أو .rev)
- جرب تحديد السنة يدوياً

### المشكلة: فشل فك التشفير

**الحل:**
- تأكد من استخدام المفتاح الصحيح للسنة
- تحقق من عدم تلف الملف
- جرب توليد مفتاح جديد

### المشكلة: خطأ في الذاكرة

**الحل:**
- أغلق التطبيقات الأخرى
- زد حجم الذاكرة الافتراضية
- قسّم الملف الكبير إلى أجزاء

### المشكلة: المفاتيح لا تعمل

**الحل:**
- تحقق من السنة المحددة
- تأكد من عدم تعديل الملف
- استخدم مولد المفاتيح المدمج

---

## دعم فني / Technical Support

للحصول على المساعدة:

- 📧 البريد: support@blk-rev-extractor.com
- 🐙 GitHub Issues: [github.com/yourusername/blk-rev-extractor/issues](https://github.com/yourusername/blk-rev-extractor/issues)
- 📖 الوثائق: [docs.blk-rev-extractor.com](https://docs.blk-rev-extractor.com)

---

**ملاحظة:** هذا البرنامج مخصص للاستخدام القانوني فقط. يجب احترام حقوق الملكية الفكرية وقوانين حماية البيانات.

**Note:** This software is intended for legal use only. Respect intellectual property rights and data protection laws.
