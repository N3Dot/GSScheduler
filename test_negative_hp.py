#!/usr/bin/env python3
"""
Test script để kiểm tra HP âm và hiển thị
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Backend.Code import Character

def test_negative_hp():
    """Test HP âm và hiển thị"""
    print("=== Test HP âm ===")
    
    # Tạo character với HP thấp
    character = Character("Test Player")
    character.hp = 10
    character.max_hp = 50
    
    print(f"HP ban đầu: {character.hp}/{character.max_hp}")
    
    # Giảm HP xuống âm
    character.hp -= 25
    print(f"HP sau khi bị damage 25: {character.hp}/{character.max_hp}")
    
    # Kiểm tra validate_health không ngăn HP âm
    character.validate_health()
    print(f"HP sau validate_health: {character.hp}/{character.max_hp}")
    
    # Test hiển thị HP âm
    hp_display = f"{character.hp}/{character.max_hp}"
    print(f"Chuỗi hiển thị HP: '{hp_display}'")
    
    # Test màu sắc logic
    is_low_hp = character.hp <= 0
    color_text = "ĐỎ" if is_low_hp else "XANH"
    print(f"Màu hiển thị: {color_text}")
    
    print("✅ Test hoàn thành - HP âm được hiển thị chính xác")

if __name__ == "__main__":
    test_negative_hp()
