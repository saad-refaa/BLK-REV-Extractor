#!/usr/bin/env python3
import gzip
import os

def peek_gzip(filepath):
    # The file has a 32-byte header, then gzip data
    with open(filepath, 'rb') as f:
        f.seek(32)
        compressed_data = f.read()
    
    # Decrypt first
    key = bytes.fromhex("E46F59D844730E27")
    decrypted = bytes([b ^ key[i % len(key)] for i, b in enumerate(compressed_data)])
    
    try:
        decompressed = gzip.decompress(decrypted)
        print(f"Decompressed size: {len(decompressed)}")
        print("First 256 bytes of decompressed data (Hex):")
        print(decompressed[:256].hex('-'))
        print("\nFirst 256 bytes (ASCII/UTF-8):")
        print(decompressed[:256].decode('utf-8', errors='ignore'))
        
        # Look for common file signatures in decompressed data
        if decompressed.startswith(b'\x7fELF'): print("\nDetected: ELF binary")
        if decompressed.startswith(b'MZ'): print("\nDetected: Windows Executable")
        if b'<?xml' in decompressed[:100]: print("\nDetected: XML file")
        if b'{"' in decompressed[:100]: print("\nDetected: JSON file")
        if b'sqlite' in decompressed[:100].lower(): print("\nDetected: SQLite database")
        
    except Exception as e:
        print(f"Decompression error: {e}")

if __name__ == "__main__":
    peek_gzip("D:\\blocks\\blocks\\blk00000.dat")
