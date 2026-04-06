#!/usr/bin/env python3
import os

def brute_force_xor(filepath, sample_size=1024):
    with open(filepath, 'rb') as f:
        f.seek(32) # Skip header
        data = f.read(sample_size)
    
    print(f"Brute forcing XOR for {filepath}...")
    results = []
    
    for key in range(256):
        decrypted = bytes([b ^ key for b in data])
        # Count printable characters
        printable = sum(1 for b in decrypted if 32 <= b < 127)
        score = printable / sample_size
        
        # Check for specific patterns like "blk", "rev", "dat", or common words
        common_words = [b"text", b"data", b"version", b"block", b"rev"]
        word_score = sum(5 for word in common_words if word in decrypted.lower())
        
        total_score = score + word_score
        
        if total_score > 0.3:
            results.append((key, total_score, decrypted[:100]))
            
    # Sort by score descending
    results.sort(key=lambda x: x[1], reverse=True)
    
    for key, score, preview in results[:5]:
        print(f"Key: 0x{key:02X} ({key}), Score: {score:.2f}")
        print(f"Preview: {preview}")
        print("-" * 50)

if __name__ == "__main__":
    import sys
    path = "D:\\blocks\\blocks\\blk00000.dat"
    if len(sys.argv) > 1:
        path = sys.argv[1]
    brute_force_xor(path)
