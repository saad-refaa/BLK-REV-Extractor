# BLK-REV Extractor Pro v1.0

أداة متخصصة لاستخراج وتحليل البيانات من ملفات BLK .DAT و REV .DAT المستخدمة في أنظمة معينة خلال الفترة 2009-2014.

A specialized tool for extracting and analyzing data from BLK .DAT and REV .DAT files used in certain systems during 2009-2014.

## المميزات / Features

- 🔓 **دعم التشفير** / Encryption Support: XOR, AES-128-CBC, AES-256-CBC, AES-256-GCM
- 📦 **فك الضغط** / Decompression: zlib, LZ4, Zstandard
- 🔑 **مولد مفاتيح** / Key Generator: Generate compatible keys for 2009-2014
- 📊 **تصدير متعدد** / Multi-format Export: CSV, Excel (XLSX), JSON, XML
- 🖥️ **واجهة سهلة** / User-friendly GUI: Arabic/English bilingual interface
- 🔍 **معاينة مباشرة** / Live Preview: View extracted data in real-time

## المتطلبات / Requirements

- Python 3.8 أو أحدث / or higher
- Windows 7/8/10/11

## التثبيت / Installation

```bash
# Clone or extract the project
cd BLK-REV-Extractor

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## الاستخدام / Usage

### 1. فتح ملف / Open File
- اختر "فتح ملف" من القائمة
- Select "Open File" from the menu
- Supported formats: `.blk`, `.rev`, `.dat`

### 2. توليد مفاتيح / Generate Keys
- اذهب إلى "أدوات > مولد المفاتيح"
- Go to "Tools > Key Generator"
- اختر السنة المناسبة (2009-2014)
- Select appropriate year (2009-2014)

### 3. استخراج البيانات / Extract Data
- اضغط على "استخراج البيانات"
- Click "Extract Data"
- سيتم فك التشفير والضغط تلقائياً
- Decryption and decompression happen automatically

### 4. تصدير النتائج / Export Results
- اختر "تصدير" من القائمة
- Select "Export" from menu
- Available formats: CSV, Excel, JSON

## هيكل المشروع / Project Structure

```
BLK-REV-Extractor/
├── backend/
│   ├── core/           # Core extraction engine
│   ├── crypto/         # Encryption and key management
│   └── exporters/      # Export modules
├── frontend/
│   ├── main_window.py  # Main GUI window
│   ├── pages/          # UI pages
│   └── components/     # UI components
├── utils/              # Utilities and helpers
├── data/signatures/    # File format signatures
├── main.py            # Entry point
└── requirements.txt   # Dependencies
```

## التوافق / Compatibility

| السنة | BLK | REV | التشفير | الضغط |
|-------|-----|-----|---------|-------|
| 2009  | ✓   | ✓   | XOR     | -     |
| 2010  | ✓   | ✓   | AES-128 | -     |
| 2011  | ✓   | ✓   | AES-256 | zlib  |
| 2012  | ✓   | ✓   | AES-256 | LZ4   |
| 2013  | ✓   | ✓   | AES-GCM | LZ4   |
| 2014  | ✓   | ✓   | AES-GCM | Zstd  |

## المساهمة / Contributing

نرحب بالمساهمات! يرجى اتباع الخطوات التالية:
Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## الترخيص / License

هذا المشروع مرخص بموجب MIT License.
This project is licensed under the MIT License.

## الدعم / Support

للإبلاغ عن مشاكل أو طلب ميزات جديدة:
To report issues or request features:

- Email: support@blk-rev-extractor.com
- Issues: [GitHub Issues](https://github.com/yourusername/blk-rev-extractor/issues)

---

**ملاحظة هامة:** / **Important Note:**
هذه الأداة مخصصة لاستعادة البيانات من الأنظمة القديمة فقط. يجب استخدامها بشكل قانوني وأخلاقي.
This tool is intended for data recovery from legacy systems only. Use it legally and ethically.
