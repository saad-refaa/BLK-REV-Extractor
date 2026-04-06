#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Integration Tests for BLK-REV Extractor
Tests complete workflows
"""

import unittest
import sys
import os
import tempfile
import struct

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.core.data_extractor import DataExtractor
from backend.core.file_reader import FileReader
from backend.core.blk_parser import BLKParser
from backend.core.rev_parser import REVParser
from backend.crypto.keygen_2009_2014 import KeyGenerator2009_2014
from backend.exporters.json_exporter import JSONExporter
from backend.exporters.csv_exporter import CSVExporter


class TestFullWorkflow(unittest.TestCase):
    """Test complete extraction workflow"""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.sample_files = []

    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def create_sample_blk_2009(self):
        """Create sample 2009 BLK file"""
        filepath = os.path.join(self.temp_dir, "sample_2009.blk")

        # Header: magic + padding
        header = b'BLK\x00' + b'\x00' * 60

        # Data block with text entry
        data = b'\x01'  # Text type marker
        text = b"Test entry 2009"
        data += struct.pack('<H', len(text))
        data += text
        data += b'\x00' * (4096 - len(data))  # Pad

        with open(filepath, 'wb') as f:
            f.write(header)
            f.write(data)

        return filepath

    def test_extract_blk_2009(self):
        """Test extracting 2009 BLK file"""
        filepath = self.create_sample_blk_2009()

        extractor = DataExtractor()
        file_info = extractor.load_file(filepath)

        self.assertEqual(file_info.file_type.value, "BLK")
        self.assertEqual(file_info.version, "2009")
        self.assertTrue(file_info.is_valid)

        # Extract
        result = extractor.extract()
        self.assertEqual(result.status.value, "completed")

    def test_key_generation_and_validation(self):
        """Test key generation workflow"""
        generator = KeyGenerator2009_2014()

        # Generate for all years
        keys = generator.generate_all_keys()
        self.assertEqual(len(keys), 6)

        # Save and reload
        key_file = os.path.join(self.temp_dir, "keys.json")
        generator.save_keys_to_file(key_file, "json")
        self.assertTrue(os.path.exists(key_file))

        # Verify file content
        import json
        with open(key_file, 'r') as f:
            data = json.load(f)
            self.assertIsInstance(data, list)
            self.assertEqual(len(data), 6)
            self.assertEqual(data[0]["year"], 2009)

    def test_export_workflow(self):
        """Test export workflow"""
        # Create sample and extract
        filepath = self.create_sample_blk_2009()

        extractor = DataExtractor()
        extractor.load_file(filepath)
        result = extractor.extract()

        # Export to JSON
        json_file = os.path.join(self.temp_dir, "output.json")
        exporter = JSONExporter()
        exporter.export_extraction_result(result, json_file)

        self.assertTrue(os.path.exists(json_file))

        # Verify JSON structure
        import json
        with open(json_file, 'r') as f:
            data = json.load(f)
            self.assertIn("file_info", data)
            self.assertIn("status", data)


class TestErrorHandling(unittest.TestCase):
    """Test error handling"""

    def test_nonexistent_file(self):
        """Test handling non-existent file"""
        extractor = DataExtractor()

        with self.assertRaises(FileNotFoundError):
            extractor.load_file("/nonexistent/file.dat")

    def test_invalid_year(self):
        """Test invalid year for key generation"""
        generator = KeyGenerator2009_2014()

        with self.assertRaises(ValueError):
            generator.generate_key(2008)  # Before 2009

        with self.assertRaises(ValueError):
            generator.generate_key(2015)  # After 2014

    def test_corrupted_file(self):
        """Test handling corrupted file"""
        import tempfile

        with tempfile.NamedTemporaryFile(delete=False, suffix='.dat') as f:
            f.write(b'CORRUPTED_DATA')
            temp_path = f.name

        try:
            reader = FileReader()
            file_type, version = reader.detect_file_type(temp_path)
            self.assertEqual(file_type.value, "UNKNOWN")
        finally:
            os.unlink(temp_path)


if __name__ == "__main__":
    unittest.main(verbosity=2)
