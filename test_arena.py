#!/usr/bin/env python3
# Test arena system

from Backend.Code import generate_demo_base64_codes

if __name__ == "__main__":
    print("Generating demo Base64 codes for Arena:")
    codes = generate_demo_base64_codes(5)
    
    for i, code in enumerate(codes, 1):
        print(f"\nDemo Code {i}:")
        print(code)
        print("-" * 50)
