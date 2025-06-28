#!/usr/bin/env python3
"""
Simple test để tạo QR code và kiểm tra format
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Backend.Code import SessionManager, Character, RewardSystem, StudyAnalytics, QuestSystem
import json
import gzip
import base64

def test_qr_formats():
    print("=== TEST QR FORMATS ===")
    
    # Tạo dữ liệu test
    char = Character("Player Test")
    char.level = 10
    char.xp = 500
    char.gold = 200
    char.dex = 5
    char.int = 7
    char.luk = 3
    
    session_manager = SessionManager(
        character=char,
        reward_system=RewardSystem(),
        analytics=StudyAnalytics(QuestSystem())
    )
    
    print(f"Test character: {char.name} (Lv.{char.level}) - Gold: {char.gold}")
    
    # Test _get_optimized_qr_data
    print("\n1. Testing _get_optimized_qr_data...")
    optimized_data = session_manager._get_optimized_qr_data()
    print(f"Optimized format: {json.dumps(optimized_data, indent=2)}")
    
    # Test _get_minimal_qr_data  
    print("\n2. Testing _get_minimal_qr_data...")
    minimal_data = session_manager._get_minimal_qr_data()
    print(f"Minimal format: {json.dumps(minimal_data, indent=2)}")
    
    # Test import with optimized format
    print("\n3. Testing import optimized format...")
    test_char1 = Character("Test1")
    test_sm1 = SessionManager(character=test_char1, reward_system=RewardSystem(), analytics=StudyAnalytics(QuestSystem()))
    
    success1 = test_sm1._load_save_data(optimized_data)
    print(f"Import success: {success1}")
    if success1:
        print(f"Result: {test_char1.name} (Lv.{test_char1.level}) - Gold: {test_char1.gold}")
    
    # Test import with minimal format
    print("\n4. Testing import minimal format...")
    test_char2 = Character("Test2")
    test_sm2 = SessionManager(character=test_char2, reward_system=RewardSystem(), analytics=StudyAnalytics(QuestSystem()))
    
    success2 = test_sm2._load_save_data(minimal_data)
    print(f"Import success: {success2}")
    if success2:
        print(f"Result: {test_char2.name} (Lv.{test_char2.level}) - Gold: {test_char2.gold}")
    
    # Test full QR generation process
    print("\n5. Testing full QR generation and import...")
    qr_path = session_manager.generate_qr_code()
    print(f"QR generated: {qr_path}")
    
    # Simulate QR data
    optimized_data = session_manager._get_optimized_qr_data()
    json_string = json.dumps(optimized_data, ensure_ascii=False, separators=(',', ':'))
    compressed_bytes = gzip.compress(json_string.encode('utf-8'))
    compressed_data = base64.b64encode(compressed_bytes).decode('ascii')
    qr_data = f"GSS:{compressed_data}"
    
    print(f"QR data length: {len(qr_data)}")
    print(f"QR data preview: {qr_data[:100]}...")
    
    # Test import từ QR data
    test_char3 = Character("Test3")
    test_sm3 = SessionManager(character=test_char3, reward_system=RewardSystem(), analytics=StudyAnalytics(QuestSystem()))
    
    success3 = test_sm3.import_from_qr_data(qr_data)
    print(f"QR Import success: {success3}")
    if success3:
        print(f"Final result: {test_char3.name} (Lv.{test_char3.level}) - Gold: {test_char3.gold}")
        print(f"Stats: DEX:{test_char3.dex} INT:{test_char3.int} LUK:{test_char3.luk}")
        
        # Kiểm tra chính xác
        if (test_char3.name == char.name and 
            test_char3.level == char.level and
            test_char3.gold == char.gold and
            test_char3.dex == char.dex and
            test_char3.int == char.int and
            test_char3.luk == char.luk):
            print("✅ QR IMPORT HOÀN TOÀN CHÍNH XÁC!")
        else:
            print("❌ QR import có sai lệch!")
    
    print("\n=== TEST HOÀN THÀNH ===")

if __name__ == "__main__":
    test_qr_formats()
