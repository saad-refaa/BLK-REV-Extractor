#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit Tests for BLK-REV Extractor
"""

import unittest
import sys
import os
import tempfile
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.core.file_reader import FileReader, FileType, FileInfo
from backend.crypto.keygen_2009_2014 import KeyGenerator2009_2014
from backend.crypto.key_validator import KeyValidator
from backend.crypto.decryption import DecryptionManager
from utils.helpers import format_bytes, format_hex, xor_data
from utils.config_manager import ConfigManager


class TestFileReader(unittest.TestCase):
    """Test file reader functionality"""

    def setUp(self):
        self.reader = FileReader()

    def test_signatures_loaded(self):
        """Test that signatures are loaded"""
        self.assertIsNotNone(self.reader.blk_signatures)
        self.assertIsNotNone(self.reader.rev_signatures)
        # Check if versions key exists and has items
        blk_versions = self.reader.blk_signatures.get("versions", {})
        self.assertGreater(len(blk_versions), 0, "No BLK signatures found")
        rev_versions = self.reader.rev_signatures.get("versions", {})
        self.assertGreater(len(rev_versions), 0, "No REV signatures found")

    def test_detect_file_type_unknown(self):
        """Test detection of unknown file"""
        # Create temp file with unknown magic
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b'XXXX')
            temp_path = f.name

        try:
            file_type, version = self.reader.detect_file_type(temp_path)
            self.assertEqual(file_type, FileType.UNKNOWN)
        finally:
            os.unlink(temp_path)


class TestKeyGenerator(unittest.TestCase):
    """Test key generation"""

    def setUp(self):
        self.generator = KeyGenerator2009_2014()

    def test_generate_key_2009(self):
        """Test generating 2009 key"""
        key = self.generator.generate_key(2009)
        self.assertEqual(key.year, 2009)
        self.assertEqual(key.algorithm, "XOR")
        self.assertGreater(len(key.key_value), 0)

    def test_generate_key_2014(self):
        """Test generating 2014 key"""
        key = self.generator.generate_key(2014)
        self.assertEqual(key.year, 2014)
        self.assertEqual(key.algorithm, "AES-256-GCM")
        self.assertEqual(len(key.key_value), 32)

    def test_generate_all_keys(self):
        """Test generating all years"""
        keys = self.generator.generate_all_keys()
        self.assertEqual(len(keys), 6)  # 2009-2014
        years = [k.year for k in keys]
        self.assertEqual(sorted(years), [2009, 2010, 2011, 2012, 2013, 2014])

    def test_key_uniqueness(self):
        """Test that keys are unique with different seeds"""
        key1 = self.generator.generate_key(2010, custom_seed="seed1")
        key2 = self.generator.generate_key(2010, custom_seed="seed2")
        self.assertNotEqual(key1.key_value, key2.key_value)


class TestKeyValidator(unittest.TestCase):
    """Test key validation"""

    def setUp(self):
        self.generator = KeyGenerator2009_2014()
        self.validator = KeyValidator()

    def test_validate_valid_key(self):
        """Test validating a valid key"""
        key = self.generator.generate_key(2010)
        result = self.validator.validate_key(key)
        self.assertTrue(result.is_valid)

    def test_validate_wrong_size(self):
        """Test detecting wrong key size"""
        key = self.generator.generate_key(2010)
        # Corrupt key size
        key.key_value = key.key_value[:8]  # Too short
        result = self.validator.validate_key(key)
        self.assertFalse(result.is_valid)
        self.assertTrue(any("size" in e.lower() for e in result.errors))


class TestDecryption(unittest.TestCase):
    """Test decryption functionality"""

    def setUp(self):
        self.manager = DecryptionManager()

    def test_xor_decrypt(self):
        """Test XOR decryption"""
        data = b'Hello World'
        key = b'\x5a'
        encrypted = xor_data(data, 0x5a)
        decrypted = self.manager.decrypt(encrypted, "XOR", key)
        self.assertEqual(decrypted, data)

    def test_xor_roundtrip(self):
        """Test XOR encryption/decryption roundtrip"""
        original = b'Test data 123'
        key = 0x42
        encrypted = xor_data(original, key)
        decrypted = xor_data(encrypted, key)
        self.assertEqual(original, decrypted)


class TestHelpers(unittest.TestCase):
    """Test helper functions"""

    def test_format_bytes(self):
        """Test byte formatting"""
        self.assertIn("KB", format_bytes(1024))
        self.assertIn("MB", format_bytes(1024*1024))
        self.assertIn("B", format_bytes(512))

    def test_format_hex(self):
        """Test hex formatting"""
        data = b'\x00\x01\x02\x03'
        hex_str = format_hex(data)
        self.assertIn("00", hex_str)
        self.assertIn("01", hex_str)

    def test_xor_data(self):
        """Test XOR operation"""
        data = b'ABC'
        result = xor_data(data, 0x00)
        self.assertEqual(result, data)

        result = xor_data(data, 0xFF)
        expected = bytes([b ^ 0xFF for b in data])
        self.assertEqual(result, expected)


class TestConfigManager(unittest.TestCase):
    """Test configuration manager"""

    def setUp(self):
        # Use temp directory for tests
        self.temp_dir = tempfile.mkdtemp()
        self.config = ConfigManager(self.temp_dir)

    def tearDown(self):
        # Cleanup
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_default_values(self):
        """Test default configuration values"""
        self.assertEqual(self.config.get("language"), "ar")
        self.assertEqual(self.config.get("theme"), "default")

    def test_set_get(self):
        """Test setting and getting values"""
        self.config.set("language", "en")
        self.assertEqual(self.config.get("language"), "en")

    def test_recent_files(self):
        """Test recent files management"""
        # ConfigManager filters files that don't exist, so we create temp ones
        with tempfile.NamedTemporaryFile(delete=False) as f1, \
             tempfile.NamedTemporaryFile(delete=False) as f2:
            f1_path = f1.name
            f2_path = f2.name
            
        try:
            self.config.add_recent_file(f1_path)
            self.config.add_recent_file(f2_path)

            recent = self.config.get_recent_files()
            self.assertEqual(len(recent), 2)
            self.assertEqual(recent[0], f2_path)  # Most recent first
        finally:
            if os.path.exists(f1_path): os.unlink(f1_path)
            if os.path.exists(f2_path): os.unlink(f2_path)


def create_test_suite():
    """Create test suite"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromTestCase(TestFileReader))
    suite.addTests(loader.loadTestsFromTestCase(TestKeyGenerator))
    suite.addTests(loader.loadTestsFromTestCase(TestKeyValidator))
    suite.addTests(loader.loadTestsFromTestCase(TestDecryption))
    suite.addTests(loader.loadTestsFromTestCase(TestHelpers))
    suite.addTests(loader.loadTestsFromTestCase(TestConfigManager))

    return suite


if __name__ == "__main__":
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    suite = create_test_suite()
    result = runner.run(suite)

    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)
