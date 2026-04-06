#!/usr/bin/env python3
import hashlib
import struct
import os
import glob

def double_sha256(data):
    return hashlib.sha256(hashlib.sha256(data).digest()).digest()

def parse_varint(data, offset):
    b = data[offset]
    if b < 0xfd:
        return b, 1
    if b == 0xfd:
        return struct.unpack('<H', data[offset+1:offset+3])[0], 3
    if b == 0xfe:
        return struct.unpack('<I', data[offset+1:offset+5])[0], 5
    if b == 0xff:
        return struct.unpack('<Q', data[offset+1:offset+9])[0], 9

def scan_file_for_tx_vulns(filepath):
    print(f"Scanning {filepath} for TXID vulnerabilities...")
    
    with open(filepath, 'rb') as f:
        raw_data = f.read()
        
    # Decrypt
    key = bytes.fromhex("E46F59D844730E27")
    data = bytes([b ^ key[i % len(key)] for i, b in enumerate(raw_data)])
    
    offset = 0
    magic = b'\xf9\xbe\xb4\xd9'
    
    all_txids = []
    
    while True:
        offset = data.find(magic, offset)
        if offset == -1:
            break
            
        try:
            # Bitcoin block format: magic(4), size(4), header(80), tx_count(varint), txs...
            block_size = struct.unpack('<I', data[offset+4:offset+8])[0]
            block_header = data[offset+8:offset+88]
            
            tx_count, varint_len = parse_varint(data, offset+88)
            curr_tx_offset = offset + 88 + varint_len
            
            block_txids = []
            
            for _ in range(tx_count):
                start_tx = curr_tx_offset
                # Simplified TX parser to find TXID
                # Version(4), Inputs(varint), Outputs(varint), Locktime(4)
                version = struct.unpack('<I', data[curr_tx_offset:curr_tx_offset+4])[0]
                curr_tx_offset += 4
                
                input_count, v_len = parse_varint(data, curr_tx_offset)
                curr_tx_offset += v_len
                for _ in range(input_count):
                    curr_tx_offset += 32 + 4 # outpoint
                    script_len, s_v_len = parse_varint(data, curr_tx_offset)
                    curr_tx_offset += s_v_len + script_len + 4 # script + sequence
                    
                output_count, v_len = parse_varint(data, curr_tx_offset)
                curr_tx_offset += v_len
                for _ in range(output_count):
                    curr_tx_offset += 8 # value
                    script_len, s_v_len = parse_varint(data, curr_tx_offset)
                    curr_tx_offset += s_v_len + script_len
                    
                curr_tx_offset += 4 # locktime
                
                tx_data = data[start_tx:curr_tx_offset]
                txid = double_sha256(tx_data)[::-1].hex()
                block_txids.append(txid)
                all_txids.append(txid)
                
            # Check for CVE-2012-2459 (Merkle Tree Malleability)
            # This happens when there's an odd number of transactions and the last one is duplicated in the Merkle tree
            if len(block_txids) > 1 and len(block_txids) % 2 == 1:
                # Merkle tree calculation would duplicate the last TXID
                pass # This is a design flaw in Merkle trees, not necessarily a vuln in this block
                
        except Exception:
            pass
            
        offset += 1
        
    # Check for duplicates across all scanned blocks
    if all_txids:
        from collections import Counter
        counts = Counter(all_txids)
        dupes = {txid: count for txid, count in counts.items() if count > 1}
        if dupes:
            print(f"  [!!!] Found {len(dupes)} duplicate TXIDs in this file!")
            for txid, count in list(dupes.items())[:5]:
                print(f"    {txid}: {count} occurrences")
        else:
            print("  No duplicate TXIDs found.")
            
    return all_txids

if __name__ == "__main__":
    files = glob.glob("D:\\blocks\\blocks\\blk*.dat")
    # Scan first few files
    total_txids = []
    for f in files[:10]:
        total_txids.extend(scan_file_for_tx_vulns(f))
        
    from collections import Counter
    counts = Counter(total_txids)
    global_dupes = {txid: count for txid, count in counts.items() if count > 1}
    if global_dupes:
        print(f"\n[SUMMARY] Found {len(global_dupes)} global duplicate TXIDs!")
