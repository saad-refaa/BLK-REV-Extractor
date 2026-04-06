#!/usr/bin/env python3
import sys

def decrypt_sample(filepath, key_bytes, output_path):
    with open(filepath, 'rb') as f:
        data = f.read(16384) # Read 16KB
    
    header = data[:32]
    payload = data[32:]
    
    decrypted = bytes([b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(payload)])
    
    with open(output_path, 'wb') as f:
        f.write(header)
        f.write(decrypted)
    
    print(f"Decrypted 16KB to {output_path}")
    
    # Look for common compression headers
    # LZ4: 04 22 4D 18
    if b'\x04"M\x18' in decrypted:
        print("Found LZ4 magic bytes!")
    # Zstd: 28 B5 2F FD
    if b'(\xb5/\xfd' in decrypted:
        print("Found Zstandard magic bytes!")
    # Gzip: 1F 8B
    if b'\x1f\x8b' in decrypted:
        print("Found Gzip magic bytes!")

if __name__ == "__main__":
    key = bytes.fromhex("E46F59D844730E27")
    decrypt_sample("D:\\blocks\\blocks\\blk00000.dat", key, "C:\\Users\\ENG Saad\\Desktop\\decrypted_sample.dat")
