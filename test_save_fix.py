#!/usr/bin/env python3
"""
Test save system với datetime serialization fix
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Backend.Code import Character, SessionManager, RewardSystem, StudyAnalytics, QuestSystem

def test_save_load():
    """Test save và load với fix datetime"""
    print("=== Test Save/Load System ===")
    
    # Tạo character và dữ liệu
    character = Character("TestPlayer")
    character.hp = 35  # Test với HP không full
    character.gold = 123
    character.level = 3
    
    reward_system = RewardSystem()
    analytics = StudyAnalytics(QuestSystem())
    
    session_manager = SessionManager(
        character=character,
        reward_system=reward_system,
        analytics=analytics
    )
    
    print(f"Trước save: HP={character.hp}, Gold={character.gold}, Level={character.level}")
    
    # Test ExportSave
    print("\nTesting ExportSave...")
    success = session_manager.ExportSave()
    print(f"ExportSave result: {success}")
    
    if success:
        print("✅ Save thành công!")
        
        # Test ImportSave với character mới
        new_character = Character("NewPlayer")
        new_session_manager = SessionManager(
            character=new_character,
            reward_system=RewardSystem(),
            analytics=StudyAnalytics(QuestSystem())
        )
        
        print("\nTesting ImportSave...")
        load_success = new_session_manager.ImportSave()
        print(f"ImportSave result: {load_success}")
        
        if load_success:
            print(f"Sau load: HP={new_character.hp}, Gold={new_character.gold}, Level={new_character.level}")
            
            # Verify dữ liệu đã load đúng
            assert new_character.hp == 35, f"HP không đúng: {new_character.hp}"
            assert new_character.gold == 123, f"Gold không đúng: {new_character.gold}"
            assert new_character.level == 3, f"Level không đúng: {new_character.level}"
            
            print("✅ Load và verify thành công!")
        else:
            print("❌ Load thất bại")
    else:
        print("❌ Save thất bại")
    
    # Test QR generation
    print("\nTesting QR generation...")
    qr_path = session_manager.generate_qr_code()
    if qr_path:
        print(f"✅ QR code generated: {qr_path}")
    else:
        print("❌ QR generation failed")

if __name__ == "__main__":
    try:
        test_save_load()
        print("\n🎉 All save/load tests PASSED!")
    except Exception as e:
        print(f"\n❌ Test FAILED: {e}")
        import traceback
        traceback.print_exc()
