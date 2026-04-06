"""
Test Sample - Example usage of BLK-REV Extractor
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.core.file_reader import FileReader, FileType
from backend.crypto.keygen_2009_2014 import KeyGenerator2009_2014
from backend.crypto.key_validator import KeyValidator


def test_key_generation():
    """Test key generation"""
    print("=" * 50)
    print("Testing Key Generation")
    print("=" * 50)

    generator = KeyGenerator2009_2014()

    # Generate keys for all years
    keys = generator.generate_all_keys()

    for key in keys:
        print(f"\nYear: {key.year}")
        print(f"  Algorithm: {key.algorithm}")
        print(f"  Key ID: {key.key_id}")
        print(f"  Key (Hex): {key.key_hex[:32]}...")
        print(f"  Valid for: {', '.join(key.valid_for)}")

    # Validate keys
    validator = KeyValidator()
    results = validator.validate_all_years()

    print(f"\nValidation Results: {sum(1 for r in results if r.is_valid)}/{len(results)} valid")

    return keys


def test_file_reader():
    """Test file reader (requires sample files)"""
    print("\n" + "=" * 50)
    print("Testing File Reader")
    print("=" * 50)

    reader = FileReader("data/signatures")

    # Check signatures loaded
    print(f"BLK signatures: {len(reader.blk_signatures.get('versions', {}))} versions")
    print(f"REV signatures: {len(reader.rev_signatures.get('versions', {}))} versions")

    return reader


def create_sample_blk_file(filepath: str, year: int = 2009):
    """Create a sample BLK file for testing"""
    import struct

    # Magic bytes based on year
    magic_map = {
        2009: b'BLK\x00',
        2010: b'BLK\x01',
        2011: b'BLK\x02',
        2012: b'BLK\x03',
        2013: b'BLK\x04',
        2014: b'BLK\x05'
    }

    magic = magic_map.get(year, b'BLK\x00')

    # Simple header
    header = magic + b'\x00' * 60  # 64 byte header

    # Sample data block
    data = b'\x01'  # Text type
    data += struct.pack('<H', 13)  # Length
    data += b'Hello, World!'  # Content
    data += b'\x00' * (4096 - len(data))  # Pad to block size

    with open(filepath, 'wb') as f:
        f.write(header)
        f.write(data)

    print(f"Created sample file: {filepath}")


def main():
    """Main test function"""
    print("BLK-REV Extractor - Component Tests")
    print("=" * 50)

    # Test key generation
    keys = test_key_generation()

    # Test file reader
    reader = test_file_reader()

    # Create sample file
    sample_dir = "test_samples"
    os.makedirs(sample_dir, exist_ok=True)

    for year in [2009, 2010, 2011]:
        filepath = f"{sample_dir}/sample_{year}.blk"
        create_sample_blk_file(filepath, year)

        # Try to read it
        try:
            info = reader.open_file(filepath)
            print(f"\nFile: {filepath}")
            print(f"  Type: {info.file_type.value}")
            print(f"  Version: {info.version}")
            print(f"  Size: {info.size} bytes")
            print(f"  Valid: {info.is_valid}")
            reader.close()
        except Exception as e:
            print(f"Error reading {filepath}: {e}")

    print("\n" + "=" * 50)
    print("Tests completed!")
    print("=" * 50)


if __name__ == "__main__":
    main()
