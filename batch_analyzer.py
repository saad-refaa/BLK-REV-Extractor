#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Batch Analyzer for BLK-REV Extractor
Analyzes all .dat files in a directory
"""

import os
import sys
import json
import argparse
from pathlib import Path

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.core.data_extractor import DataExtractor
from backend.crypto.keygen_2009_2014 import KeyGenerator2009_2014
from backend.exporters.json_exporter import JSONExporter

def analyze_directory(input_dir, output_dir):
    """Analyze all .dat files in directory"""
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    extractor = DataExtractor()
    keygen = KeyGenerator2009_2014()
    exporter = JSONExporter()

    # Generate keys for all years to try
    keys = keygen.generate_all_keys()

    files = list(input_path.glob("*.dat"))
    print(f"Found {len(files)} .dat files in {input_dir}")

    summary = {
        "total_files": len(files),
        "processed": 0,
        "successful": 0,
        "failed": 0,
        "results": []
    }

    for i, file_path in enumerate(files):
        print(f"[{i+1}/{len(files)}] Analyzing {file_path.name}...", end="", flush=True)
        
        try:
            file_info = extractor.load_file(str(file_path))
            
            # Try to extract with appropriate key if encrypted
            result = None
            if not file_info.is_valid:
                print(" [Invalid Format]")
                summary["failed"] += 1
                continue

            # Try different keys based on detected version
            target_year = None
            if "2009" in file_info.version:
                target_year = 2009
            else:
                try:
                    target_year = int(file_info.version)
                except:
                    pass

            if target_year and 2009 <= target_year <= 2014:
                key = keygen.generate_key(target_year).key_value
                result = extractor.extract(key)
            else:
                # Try without key
                result = extractor.extract()

            if result and result.status.value == "completed":
                # Save individual result
                out_file = output_path / f"{file_path.stem}_result.json"
                exporter.export_extraction_result(result, str(out_file))
                
                print(f" [Success: {len(result.extracted_text)} texts, {len(result.extracted_numbers)} numbers]")
                summary["successful"] += 1
                
                summary["results"].append({
                    "file": file_path.name,
                    "type": file_info.file_type.value,
                    "version": file_info.version,
                    "texts": len(result.extracted_text),
                    "numbers": len(result.extracted_numbers),
                    "output": str(out_file)
                })
            else:
                print(" [Extraction Failed]")
                summary["failed"] += 1

        except Exception as e:
            print(f" [Error: {str(e)}]")
            summary["failed"] += 1
        
        summary["processed"] += 1

    # Save summary
    with open(output_path / "batch_summary.json", 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\nBatch analysis complete!")
    print(f"Processed: {summary['processed']}")
    print(f"Successful: {summary['successful']}")
    print(f"Failed: {summary['failed']}")
    print(f"Summary saved to {output_path / 'batch_summary.json'}")

def main():
    parser = argparse.ArgumentParser(description="Batch Analyze BLK/REV files")
    parser.add_argument("-i", "--input", default="D:\\blocks\\blocks", help="Input directory")
    parser.add_argument("-o", "--output", default="analysis_results", help="Output directory")
    
    args = parser.parse_args()
    analyze_directory(args.input, args.output)

if __name__ == "__main__":
    main()
