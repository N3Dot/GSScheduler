#!/usr/bin/env python3
"""
Test script để kiểm tra QR import/export
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Backend.Code import SessionManager, Character, RewardSystem, StudyAnalytics, QuestSystem

def test_qr_import_export():
    print("=== TEST QR IMPORT/EXPORT ===")
    
    # Tạo session manager gốc với dữ liệu test
    print("\n1. Tạo dữ liệu gốc...")
    original_char = Character("Test Hero")
    original_char.level = 5
    original_char.xp = 250
    original_char.hp = 80
    original_char.max_hp = 100
    original_char.gold = 150
    original_char.dex = 3
    original_char.int = 4
    original_char.luk = 2
    original_char.available_points = 1
    original_char.unlocked_achievements = {"achievement1", "achievement2"}
    
    quest_system = QuestSystem()
    analytics = StudyAnalytics(quest_system)
    analytics.focus_streak = 5
    analytics.aggregated_stats = {
        'total_sessions': 10,
        'total_study_hours': 25.5,
        'quests_completed': 15,
        'rank_counts': {'S': 2, 'A': 3, 'B': 4, 'C': 1, 'F': 0}
    }
    
    original_session_manager = SessionManager(
        character=original_char,
        reward_system=RewardSystem(),
        analytics=analytics
    )
    
    print(f"Original character: {original_char.name} (Lv.{original_char.level})")
    print(f"HP: {original_char.hp}/{original_char.max_hp}, Gold: {original_char.gold}")
    print(f"Stats: DEX:{original_char.dex} INT:{original_char.int} LUK:{original_char.luk}")
    print(f"Achievements: {len(original_char.unlocked_achievements)}")
    print(f"Analytics: {analytics.focus_streak} streak, {analytics.aggregated_stats['total_sessions']} sessions")
    
    # Tạo QR code
    print("\n2. Tạo QR code...")
    qr_path = original_session_manager.generate_qr_code()
    print(f"QR created at: {qr_path}")
    
    # Đọc QR data từ file QR
    print("\n3. Đọc dữ liệu QR...")
    try:
        import qrcode
        from PIL import Image
        from pyzbar import pyzbar
        
        # Đọc QR từ file
        qr_image = Image.open(qr_path)
        decoded_objects = pyzbar.decode(qr_image)
        
        if decoded_objects:
            qr_data = decoded_objects[0].data.decode('utf-8')
            print(f"QR data extracted: {qr_data[:100]}...")
        else:
            print("Không đọc được QR code từ file!")
            return False
            
    except ImportError:
        print("Không có pyzbar, sử dụng dữ liệu từ generate_qr_code...")
        # Tạo lại QR data từ optimized data
        import json
        import gzip
        import base64
        
        save_data = original_session_manager._get_optimized_qr_data()
        json_string = json.dumps(save_data, ensure_ascii=False, separators=(',', ':'))
        compressed_bytes = gzip.compress(json_string.encode('utf-8'))
        compressed_data = base64.b64encode(compressed_bytes).decode('ascii')
        qr_data = f"GSS:{compressed_data}"
        print(f"QR data generated: {qr_data[:100]}...")
    
    # Tạo session manager mới để import
    print("\n4. Import vào session manager mới...")
    new_char = Character("Empty")
    new_session_manager = SessionManager(
        character=new_char,
        reward_system=RewardSystem(),
        analytics=StudyAnalytics(QuestSystem())
    )
    
    print(f"Before import: {new_char.name} (Lv.{new_char.level})")
    
    # Import dữ liệu
    success = new_session_manager.import_from_qr_data(qr_data)
    
    if success:
        print(f"\n5. Import thành công!")
        print(f"After import: {new_char.name} (Lv.{new_char.level})")
        print(f"HP: {new_char.hp}/{new_char.max_hp}, Gold: {new_char.gold}")
        print(f"Stats: DEX:{new_char.dex} INT:{new_char.int} LUK:{new_char.luk}")
        print(f"Achievements: {len(new_char.unlocked_achievements)}")
        print(f"Analytics: {new_session_manager.analytics.focus_streak} streak, {new_session_manager.analytics.aggregated_stats['total_sessions']} sessions")
        
        # So sánh
        print("\n6. Kiểm tra tính chính xác:")
        checks = [
            ("Name", original_char.name, new_char.name),
            ("Level", original_char.level, new_char.level),
            ("HP", original_char.hp, new_char.hp),
            ("Max HP", original_char.max_hp, new_char.max_hp),
            ("Gold", original_char.gold, new_char.gold),
            ("DEX", original_char.dex, new_char.dex),
            ("INT", original_char.int, new_char.int),
            ("LUK", original_char.luk, new_char.luk),
            ("Focus Streak", analytics.focus_streak, new_session_manager.analytics.focus_streak),
        ]
        
        all_correct = True
        for check_name, original, imported in checks:
            if original == imported:
                print(f"✓ {check_name}: {imported}")
            else:
                print(f"✗ {check_name}: {original} -> {imported}")
                all_correct = False
        
        if all_correct:
            print("\n🎉 TẤT CẢ DỮ LIỆU IMPORT CHÍNH XÁC!")
        else:
            print("\n❌ CÓ LỖI TRONG VIỆC IMPORT!")
        
        return all_correct
    else:
        print("❌ Import thất bại!")
        return False

if __name__ == "__main__":
    test_qr_import_export()
