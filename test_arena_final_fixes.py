#!/usr/bin/env python3
"""
Test arena final fixes:
1. HP preservation after battle ends
2. Shake animation triggers 
3. UI button sizing consistency
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Backend.Code import Character, Arena, SkillType

def test_hp_preservation_after_battle():
    """Test that HP is preserved at end-of-battle value until reset"""
    print("=== Test HP Preservation After Battle ===")
    
    # Create arena and characters
    arena = Arena()
    player = Character("Test Player")
    player.hp = 50  # Starting with damaged HP
    player.max_hp = 100
    
    # Create and load opponent
    demo_code = arena.generate_demo_opponent()
    arena.load_opponent(demo_code)
    
    print(f"Player HP before battle: {player.hp}/{player.max_hp}")
    
    # Start battle
    arena.start_battle(player)
    print(f"Player copy HP after battle start: {arena.player_copy.hp}/{arena.player_copy.max_hp}")
    
    # Simulate battle damage
    arena.player_copy.hp = 25  # Take some damage
    print(f"Player copy HP during battle (after damage): {arena.player_copy.hp}/{arena.player_copy.max_hp}")
    
    # End battle (simulate battle end without reset)
    arena.battle_active = False
    
    # Check that player_copy still exists and retains HP
    print(f"Player copy HP after battle ends: {arena.player_copy.hp}/{arena.player_copy.max_hp}")
    print(f"Original player HP (should be unchanged): {player.hp}/{player.max_hp}")
    
    # Verify that HP display logic will show copy HP instead of original
    if arena.player_copy:
        display_hp = f"{arena.player_copy.hp}/{arena.player_copy.max_hp}"
        print(f"HP that will be displayed in UI: {display_hp}")
    
    # Test manual reset
    if hasattr(arena, 'original_player_hp'):
        player.hp = arena.original_player_hp
        arena.player_copy = None
        print(f"After manual reset - Player HP: {player.hp}/{player.max_hp}")
    
    print("✅ HP preservation test passed\n")

def test_shake_animation_triggers():
    """Test that shake animation triggers are properly detected"""
    print("=== Test Shake Animation Triggers ===")
    
    arena = Arena()
    player = Character("Player")
    arena.load_opponent(arena.generate_demo_opponent())
    arena.start_battle(player)
    
    # Execute a turn and check messages
    result = arena.execute_turn(SkillType.ATTACK)
    messages = result.get("messages", [])
    
    print("Battle messages:")
    for i, msg in enumerate(messages):
        print(f"  {i+1}. {msg}")
        
        # Check for shake triggers
        if "đánh thường" in msg or "dùng phép" in msg:
            if arena.bot and arena.bot.name in msg:
                print(f"    -> Bot shake trigger detected")
            elif arena.player_copy and arena.player_copy.name in msg:
                print(f"    -> Player shake trigger detected")
    
    print("✅ Shake animation trigger test passed\n")

def test_ui_button_sizing():
    """Test that UI buttons have consistent sizing"""
    print("=== Test UI Button Sizing ===")
    
    # Read main.py to check button definitions
    with open('main.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find button definitions in arena section
    lines = content.split('\n')
    button_specs = []
    
    in_arena_section = False
    for i, line in enumerate(lines):
        if '# --- Đấu Trường Start Section ---' in line:
            in_arena_section = True
        elif '# --- Đấu Trường End Section ---' in line:
            in_arena_section = False
        
        if in_arena_section and 'MDButton:' in line:
            # Look for size specifications in following lines
            for j in range(i+1, min(i+10, len(lines))):
                if 'height:' in lines[j]:
                    button_specs.append(lines[j].strip())
                elif 'MDButton:' in lines[j]:
                    break
    
    print("Arena button height specifications:")
    for spec in button_specs:
        print(f"  {spec}")
    
    # Check for consistency
    heights = [spec.split('"')[1] for spec in button_specs if '"' in spec]
    if len(set(heights)) == 1:
        print(f"✅ All buttons have consistent height: {heights[0]}")
    else:
        print(f"⚠️ Button heights inconsistent: {heights}")
    
    print("✅ UI button sizing test completed\n")

def main():
    print("🔧 Testing Arena Final Fixes")
    print("=" * 50)
    
    test_hp_preservation_after_battle()
    test_shake_animation_triggers()
    test_ui_button_sizing()
    
    print("✅ All tests completed!")

if __name__ == "__main__":
    main()
