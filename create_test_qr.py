#!/usr/bin/env python3
"""
Tạo QR code thật để test trong app
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Backend.Code import SessionManager, Character, RewardSystem, StudyAnalytics, QuestSystem
import json
import gzip
import base64

def create_test_qr():
    print("=== TẠO QR CODE TEST ===")
    
    # Tạo nhân vật với dữ liệu thú vị
    char = Character("Siêu Học Giả")
    char.level = 15
    char.xp = 750
    char.hp = 90
    char.max_hp = 120
    char.gold = 500
    char.dex = 8
    char.int = 12
    char.luk = 6
    char.available_points = 3
    char.unlocked_achievements = {"ChamChiCanCu", "BacThayNhiemVu", "Chuoi3Ngay"}
    
    # Tạo analytics phong phú
    quest_system = QuestSystem()
    analytics = StudyAnalytics(quest_system)
    analytics.focus_streak = 7
    analytics.aggregated_stats = {
        'total_sessions': 25,
        'total_study_hours': 48.5,
        'quests_completed': 35,
        'rank_counts': {'S': 5, 'A': 8, 'B': 7, 'C': 4, 'F': 1},
        'average_session_duration_minutes': 116.4,
        'average_rank_score': 3.2,
        'quest_completion_rate': 0.92
    }
    
    session_manager = SessionManager(
        character=char,
        reward_system=RewardSystem(),
        analytics=analytics
    )
    
    print(f"Nhân vật: {char.name}")
    print(f"Level: {char.level} | XP: {char.xp}")
    print(f"HP: {char.hp}/{char.max_hp} | Gold: {char.gold}")
    print(f"Stats: DEX:{char.dex} INT:{char.int} LUK:{char.luk} | Points: {char.available_points}")
    print(f"Achievements: {len(char.unlocked_achievements)}")
    print(f"Study Stats: {analytics.focus_streak} streak, {analytics.aggregated_stats['total_sessions']} sessions")
    print(f"Total hours: {analytics.aggregated_stats['total_study_hours']}")
    
    # Tạo QR code
    print("\nTạo QR code...")
    qr_path = session_manager.generate_qr_code()
    print(f"QR code đã tạo tại: {qr_path}")
    
    # Tạo Base64 string để copy/paste
    optimized_data = session_manager._get_optimized_qr_data()
    json_string = json.dumps(optimized_data, ensure_ascii=False, separators=(',', ':'))
    compressed_bytes = gzip.compress(json_string.encode('utf-8'))
    compressed_data = base64.b64encode(compressed_bytes).decode('ascii')
    qr_data = f"GSS:{compressed_data}"
    
    print(f"\nMã Base64 để test trong app:")
    print("=" * 50)
    print(qr_data)
    print("=" * 50)
    print(f"Độ dài: {len(qr_data)} ký tự")
    
    # Test import để đảm bảo hoạt động
    print("\nKiểm tra import...")
    test_char = Character("Test")
    test_sm = SessionManager(character=test_char, reward_system=RewardSystem(), analytics=StudyAnalytics(QuestSystem()))
    
    success = test_sm.import_from_qr_data(qr_data)
    if success:
        print(f"✅ Import thành công: {test_char.name} (Lv.{test_char.level})")
        print(f"   Gold: {test_char.gold} | Stats: {test_char.dex}-{test_char.int}-{test_char.luk}")
        print(f"   Analytics: {test_sm.analytics.focus_streak} streak, {test_sm.analytics.aggregated_stats['total_sessions']} sessions")
        
        # So sánh
        if (test_char.name == char.name and test_char.level == char.level and
            test_char.gold == char.gold and test_char.dex == char.dex):
            print("✅ Dữ liệu chính xác!")
        else:
            print("❌ Có sai lệch dữ liệu!")
    else:
        print("❌ Import thất bại!")
    
    print(f"\n🎯 Hãy copy mã Base64 trên và paste vào ô 'Load dữ liệu từ QR' trong app!")
    
    return qr_data

if __name__ == "__main__":
    create_test_qr()
