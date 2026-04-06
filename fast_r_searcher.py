#!/usr/bin/env python3
import os
import mmap
import re
import multiprocessing
from collections import defaultdict
import glob

# XOR Key discovered earlier
XOR_KEY = bytes.fromhex("E46F59D844730E27")

# ECDSA DER signature patterns:
# 30 44 02 20 [32 bytes of R] 02 20 [32 bytes of S] [sighash]
# 30 45 02 21 00 [32 bytes of R] 02 20 [32 bytes of S] [sighash]
# We'll use a regex to find these patterns in the decrypted data
# 0x30 0x44 0x02 0x20 matches most standard 32-byte R values
PATTERN_32 = re.compile(rb'\x30\x44\x02\x20(.{32})\x02\x20')
PATTERN_33 = re.compile(rb'\x30\x45\x02\x21\x00(.{32})\x02\x20')

def scan_file(filepath):
    """Scan a single file for R values"""
    r_values = []
    
    try:
        with open(filepath, 'rb') as f:
            # Read in chunks to avoid memory issues and speed up decryption
            chunk_size = 1024 * 1024 # 1MB
            key_len = len(XOR_KEY)
            
            offset = 0
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                
                # Fast XOR decryption for this chunk
                # We need to account for the key offset relative to the file
                decrypted = bytearray(len(chunk))
                for i in range(len(chunk)):
                    decrypted[i] = chunk[i] ^ XOR_KEY[(offset + i) % key_len]
                
                # Find R values in this chunk
                # We search the decrypted bytearray
                for match in PATTERN_32.finditer(decrypted):
                    r_values.append(match.group(1).hex())
                for match in PATTERN_33.finditer(decrypted):
                    r_values.append(match.group(1).hex())
                
                offset += len(chunk)
                # Overlap a bit to not miss patterns split across chunks
                if len(chunk) == chunk_size:
                    f.seek(f.tell() - 100)
                    offset -= 100
                    
    except Exception as e:
        print(f"Error scanning {filepath}: {e}")
        
    return r_values

def main():
    dat_files = glob.glob("D:\\blocks\\blocks\\blk*.dat")
    print(f"Starting high-speed scan of {len(dat_files)} files...")
    
    # Use all available CPU cores
    num_cores = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=num_cores)
    
    all_r_values = defaultdict(list)
    
    # Process files in smaller batches to show progress and avoid timeout
    batch_size = 10
    for i in range(0, len(dat_files), batch_size):
        batch = dat_files[i:i+batch_size]
        print(f"Processing batch {i//batch_size + 1}/{(len(dat_files)-1)//batch_size + 1} ({len(batch)} files)...")
        results = pool.map(scan_file, batch)
        
        for j, file_r_list in enumerate(results):
            filename = os.path.basename(batch[j])
            for r in file_r_list:
                all_r_values[r].append(filename)
            
    # Check for vulnerabilities (R-value reuse)
    vulns_found = 0
    print("\n" + "="*60)
    print("VULNERABILITY REPORT: REUSED R-VALUES (NONCE REUSE)")
    print("="*60)
    
    for r, locations in all_r_values.items():
        if len(locations) > 1:
            # Filter out duplicates within the same file if they are too frequent (might be false positives)
            unique_files = sorted(list(set(locations)))
            if len(unique_files) > 1 or len(locations) > 2:
                vulns_found += 1
                print(f"[!] REUSE DETECTED: R = {r}")
                print(f"    Count: {len(locations)}")
                print(f"    Files: {', '.join(unique_files[:5])}" + ("..." if len(unique_files) > 5 else ""))
                
    if vulns_found == 0:
        print("No R-value reuse vulnerabilities found.")
    else:
        print(f"\nTotal unique R-value reuse cases found: {vulns_found}")
    print("="*60)

if __name__ == "__main__":
    main()
