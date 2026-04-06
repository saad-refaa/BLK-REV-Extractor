# Changelog

## [1.0.0] - 2024-01-15

### Added
- Initial release of BLK-REV Extractor Pro
- Support for BLK .DAT and REV .DAT files (2009-2014)
- Key generator for years 2009-2014
- Decryption support: XOR, AES-128-CBC, AES-256-CBC, AES-256-GCM
- Decompression support: zlib, LZ4, Zstandard
- Export formats: CSV, Excel (XLSX), JSON, XML
- Bilingual interface (Arabic/English)
- Command line interface (CLI)
- Graphical user interface (GUI)

### Security
- Secure key generation using PBKDF2
- Key validation system
- Safe memory handling for sensitive data

## [0.9.0] - 2024-01-01 (Beta)

### Added
- Beta testing release
- Core extraction engine
- Basic GUI implementation
- File format detection

### Known Issues
- Limited support for 2014 format variations
- Memory usage optimization needed for large files
