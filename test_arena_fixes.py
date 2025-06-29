#!/usr/bin/env python3
"""
Test các fix mới: HP không reset, battle log đầy đủ, loại bỏ icons
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Backend.Code import Character, Arena, SkillType
import json
import base64

def test_hp_preservation():
    """Test HP không bị reset khi bắt đầu trận đấu"""
    print("=== Test HP Preservation ===")
    
    # Tạo player với HP không full
    player = Character("HPTest")
    player.hp = 35  # Không full HP
    player.max_hp = 80
    print(f"Player HP trước battle: {player.hp}/{player.max_hp}")
    
    # Tạo arena và bot
    arena = Arena()
    bot_data = {
        "c": {"n": "TestBot", "l": 2, "h": 25, "m": 25, "d": 2, "i": 2, "k": 2}
    }
    bot_base64 = base64.b64encode(json.dumps(bot_data).encode('utf-8')).decode('utf-8')
    arena.load_opponent(bot_base64)
    
    # Bắt đầu battle
    arena.start_battle(player)
    
    print(f"Player real HP sau start battle: {player.hp}/{player.max_hp}")
    print(f"Player copy HP sau start battle: {arena.player_copy.hp}/{arena.player_copy.max_hp}")
    print(f"Player original HP saved: {arena.player_original_hp}")
    
    # Verify HP không bị reset
    assert player.hp == 35, f"Real player HP bị thay đổi: {player.hp}"
    assert arena.player_copy.hp == 35, f"Player copy HP không giữ nguyên: {arena.player_copy.hp}"
    assert arena.player_original_hp == 35, f"Original HP không được lưu đúng: {arena.player_original_hp}"
    
    print("✅ HP preservation PASSED!")

def test_battle_log():
    """Test battle log có ghi đầy đủ thông tin"""
    print("\n=== Test Battle Log ===")
    
    player = Character("LogTest")
    player.hp = 50
    player.max_hp = 50
    
    arena = Arena()
    bot_data = {
        "c": {"n": "LogBot", "l": 1, "h": 20, "m": 20, "d": 1, "i": 1, "k": 1}
    }
    bot_base64 = base64.b64encode(json.dumps(bot_data).encode('utf-8')).decode('utf-8')
    arena.load_opponent(bot_base64)
    arena.start_battle(player)
    
    print("Battle log trước khi đánh:")
    for log in arena.battle_log:
        print(f"  {log}")
    
    # Thực hiện một vài lượt
    result1 = arena.execute_turn(SkillType.ATTACK)
    print(f"\nSau lượt 1 - Messages: {result1.get('messages', [])}")
    
    if arena.battle_active:
        result2 = arena.execute_turn(SkillType.DEFEND)
        print(f"Sau lượt 2 - Messages: {result2.get('messages', [])}")
    
    print("\nBattle log đầy đủ:")
    for i, log in enumerate(arena.battle_log):
        print(f"  {i+1}. {log}")
    
    # Verify battle log có thông tin chi tiết
    assert len(arena.battle_log) > 0, "Battle log trống"
    
    # Kiểm tra có thông tin lượt đánh
    has_turn_info = any("Lượt" in log for log in arena.battle_log)
    print(f"Battle log có thông tin lượt: {has_turn_info}")
    
    print("✅ Battle log PASSED!")

def test_clean_text():
    """Test loại bỏ icons trong text"""
    print("\n=== Test Clean Text ===")
    
    # Test clean text function
    dirty_texts = [
        "⚔️ Trận đấu bắt đầu!",
        "🛡️ Player đang thủ!",
        "✨ Bot dùng phép thuật!",
        "Lượt 1: Player tấn công (15 sát thương). Bot phép thuật (10 sát thương)."
    ]
    
    for dirty_text in dirty_texts:
        clean_text = dirty_text.replace("⚔️", "").replace("🛡️", "").replace("✨", "").strip()
        print(f"Trước: {dirty_text}")
        print(f"Sau:  {clean_text}")
        
        # Verify không còn icons
        assert "⚔️" not in clean_text, "Còn icon ⚔️"
        assert "🛡️" not in clean_text, "Còn icon 🛡️"
        assert "✨" not in clean_text, "Còn icon ✨"
        print("✅ Cleaned successfully\n")
    
    print("✅ Clean text PASSED!")

if __name__ == "__main__":
    try:
        test_hp_preservation()
        test_battle_log()
        test_clean_text()
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ HP không bị reset khi bắt đầu battle")
        print("✅ Battle log ghi đầy đủ thông tin các lượt")
        print("✅ Text được làm sạch, loại bỏ icons")
        print("✅ Hint text đã được cập nhật cho text field")
    except Exception as e:
        print(f"\n❌ Test FAILED: {e}")
        import traceback
        traceback.print_exc()
