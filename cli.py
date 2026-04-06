#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BLK-REV Extractor - Command Line Interface
"""

import argparse
import sys
import os

# Add parent to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.core.data_extractor import DataExtractor
from backend.crypto.keygen_2009_2014 import KeyGenerator2009_2014
from backend.exporters.csv_exporter import CSVExporter
from backend.exporters.json_exporter import JSONExporter
from backend.exporters.excel_exporter import ExcelExporter


def main():
    parser = argparse.ArgumentParser(
        description="BLK-REV Extractor Pro - Extract data from BLK/REV files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s extract -i file.blk -o output.csv
  %(prog)s keys --year 2012 --output keys.json
  %(prog)s info -i file.rev
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Extract command
    extract_parser = subparsers.add_parser("extract", help="Extract data from file")
    extract_parser.add_argument("-i", "--input", required=True, help="Input file path")
    extract_parser.add_argument("-o", "--output", required=True, help="Output file path")
    extract_parser.add_argument("-f", "--format", choices=["csv", "json", "excel"], 
                               default="json", help="Output format")
    extract_parser.add_argument("-k", "--key", help="Decryption key (hex)")
    extract_parser.add_argument("-y", "--year", type=int, choices=range(2009, 2015),
                               help="File year for auto key generation")

    # Keys command
    keys_parser = subparsers.add_parser("keys", help="Generate encryption keys")
    keys_parser.add_argument("-y", "--year", type=int, choices=range(2009, 2015),
                            help="Generate key for specific year")
    keys_parser.add_argument("--all", action="store_true", help="Generate all years")
    keys_parser.add_argument("-o", "--output", help="Output file path")
    keys_parser.add_argument("-f", "--format", choices=["json", "text"], default="json")

    # Info command
    info_parser = subparsers.add_parser("info", help="Show file information")
    info_parser.add_argument("-i", "--input", required=True, help="Input file path")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    try:
        if args.command == "extract":
            return cmd_extract(args)
        elif args.command == "keys":
            return cmd_keys(args)
        elif args.command == "info":
            return cmd_info(args)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    return 0


def cmd_extract(args):
    """Handle extract command"""
    print(f"Extracting data from: {args.input}")

    extractor = DataExtractor()

    # Load file
    file_info = extractor.load_file(args.input)
    print(f"File type: {file_info.file_type.value}")
    print(f"Version: {file_info.version}")
    print(f"Size: {file_info.size:,} bytes")

    # Get key if needed
    key = None
    if args.key:
        key = bytes.fromhex(args.key)
    elif args.year:
        generator = KeyGenerator2009_2014()
        gen_key = generator.generate_key(args.year)
        key = gen_key.key_value
        print(f"Using generated key for {args.year}")

    # Extract
    result = extractor.extract(key)

    print(f"\nExtraction results:")
    print(f"  Text entries: {len(result.extracted_text)}")
    print(f"  Numeric entries: {len(result.extracted_numbers)}")
    print(f"  Status: {result.status.value}")

    # Export
    if args.format == "csv":
        exporter = CSVExporter()
        exporter.export_summary(result, args.output)
    elif args.format == "json":
        exporter = JSONExporter()
        exporter.export_extraction_result(result, args.output)
    elif args.format == "excel":
        exporter = ExcelExporter()
        if hasattr(result.data, 'text_entries'):
            exporter.export_blk_data(result.data, args.output)
        else:
            exporter.export_rev_data(result.data, args.output)

    print(f"\nOutput saved to: {args.output}")
    return 0


def cmd_keys(args):
    """Handle keys command"""
    generator = KeyGenerator2009_2014()

    if args.all:
        keys = generator.generate_all_keys()
        print(f"Generated {len(keys)} keys for years 2009-2014")
    elif args.year:
        key = generator.generate_key(args.year)
        keys = [key]
        print(f"Generated key for {args.year}:")
        print(f"  ID: {key.key_id}")
        print(f"  Algorithm: {key.algorithm}")
        print(f"  Key (Hex): {key.key_hex}")
    else:
        print("Please specify --year or --all")
        return 1

    if args.output:
        generator.save_keys_to_file(args.output, args.format)
        print(f"Keys saved to: {args.output}")

    return 0


def cmd_info(args):
    """Handle info command"""
    extractor = DataExtractor()
    file_info = extractor.load_file(args.input)

    print(f"File Information:")
    print(f"  Path: {file_info.path}")
    print(f"  Type: {file_info.file_type.value}")
    print(f"  Version: {file_info.version}")
    print(f"  Size: {file_info.size:,} bytes")
    print(f"  Header Size: {file_info.header_size} bytes")
    print(f"  Block Size: {file_info.block_size} bytes")
    print(f"  Encryption: {file_info.encryption_type}")
    print(f"  Valid: {file_info.is_valid}")

    if file_info.errors:
        print(f"\nErrors:")
        for error in file_info.errors:
            print(f"  - {error}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
