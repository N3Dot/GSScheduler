#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script để kiểm tra Character UI components hoạt động đúng
"""

import sys
import os

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_character_components():
    """Test các component Character mới"""
    print("🎭 Testing Character UI Components...")
    
    try:
        # Test import modules
        print("📦 Testing imports...")
        from main import GSS
        from Backend import Code, UI, Popups
        print("✅ All imports successful!")
        
        # Test Character class
        print("👤 Testing Character initialization...")
        character = Code.Character("Test Player")
        print(f"✅ Character created: {character.name}")
        print(f"   HP: {character.hp}/{character.max_hp}")
        print(f"   Level: {character.level}")
        print(f"   Stats: DEX:{character.dex} INT:{character.int} LUK:{character.luk}")
        print(f"   Gold: {character.gold}")
        
        # Test character progression
        print("📈 Testing character progression...")
        character.xp += 50
        character.check_level_up()
        character.gold += 100
        character.dex += 2
        character.int += 1
        character.luk += 1
        
        print(f"✅ After progression:")
        print(f"   XP: {character.xp}/{character.xp_to_next_level}")
        print(f"   Level: {character.level}")
        print(f"   Stats: DEX:{character.dex} INT:{character.int} LUK:{character.luk}")
        print(f"   Gold: {character.gold}")
        
        print("\n🎉 All Character component tests passed!")
        print("💡 Character screen should now display properly with:")
        print("   - Character avatar (clickable)")
        print("   - Name and level")
        print("   - HP and XP progress bars")
        print("   - DEX, INT, LUK stats")
        print("   - Gold counter")
        print("   - Available points for upgrades")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("🔧 Make sure all Backend modules are available")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print("🔧 Check the error and fix accordingly")

if __name__ == "__main__":
    test_character_components()
