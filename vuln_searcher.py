#!/usr/bin/env python3
import os
import json
import glob

def search_vulns(results_dir):
    print(f"Searching for vulnerabilities in {results_dir}...")
    
    keywords = ["vuln", "txid", "malleable", "duplicate", "exploit", "cve", "attack", "bug"]
    found_any = False
    
    for filepath in glob.glob(os.path.join(results_dir, "*.json")):
        if "batch_summary" in filepath:
            continue
            
        with open(filepath, 'r') as f:
            try:
                data = json.load(f)
            except:
                continue
                
            file_name = data.get("file_info", {}).get("path", filepath)
            
            # Search in extracted text
            text_entries = data.get("extracted_text_preview", [])
            for text in text_entries:
                found_keywords = [k for k in keywords if k in text.lower()]
                if found_keywords:
                    print(f"\n[!] Found potential mention in {file_name}:")
                    print(f"    Keywords: {found_keywords}")
                    print(f"    Content: {text[:200]}...")
                    found_any = True
                    
            # Search for duplicate TXIDs if we had a way to identify them
            # For now, let's just look for 64-char hex strings which might be TXIDs
            import re
            txid_pattern = re.compile(r'\b[0-9a-fA-F]{64}\b')
            
            all_text = " ".join(text_entries)
            found_txids = txid_pattern.findall(all_text)
            if found_txids:
                # Check for duplicates within the file
                unique_txids = set(found_txids)
                if len(unique_txids) < len(found_txids):
                    print(f"\n[!!!] Duplicate TXIDs found in {file_name}!")
                    from collections import Counter
                    counts = Counter(found_txids)
                    for txid, count in counts.items():
                        if count > 1:
                            print(f"    TXID: {txid} (Count: {count})")
                    found_any = True

    if not found_any:
        print("No obvious vulnerability mentions or duplicate TXIDs found in extracted text.")

if __name__ == "__main__":
    search_vulns("C:\\Users\\ENG Saad\\Desktop\\analysis_results")
