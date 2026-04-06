#!/usr/bin/env python3
import os

def find_gzip_chunks(filepath):
    with open(filepath, 'rb') as f:
        data = f.read(1024 * 1024) # 1MB sample
    
    key = bytes.fromhex("E46F59D844730E27")
    decrypted = bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])
    
    offset = 0
    while True:
        offset = decrypted.find(b'\x1f\x8b\x08', offset)
        if offset == -1:
            break
        print(f"Found potential Gzip header at offset {offset}")
        offset += 1

if __name__ == "__main__":
    find_gzip_chunks("D:\\blocks\\blocks\\blk00000.dat")
