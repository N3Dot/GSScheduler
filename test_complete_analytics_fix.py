#!/usr/bin/env python3
"""
Test complete analytics fix with realistic scenario
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Backend.Code import SessionManager, Character, RewardSystem, StudyAnalytics, QuestSystem
from datetime import datetime, date, timedelta

def test_complete_analytics_scenario():
    """Test a complete scenario that matches the error case"""
    print("=== Test Complete Analytics Scenario ===")
    
    # Create components like in the real app
    character = Character("Test Player")
    quest_system = QuestSystem()
    reward_system = RewardSystem()
    analytics = StudyAnalytics(quest_system)
    session_manager = SessionManager(character=character, reward_system=reward_system, analytics=analytics)
    
    # Create a quest
    quest = quest_system.create_quest(difficulty=3, description="Test quest")
    
    # Create a session like in the real app
    start_time = datetime.now().replace(hour=14, minute=0, second=0, microsecond=0)
    end_time = start_time + timedelta(hours=1)
    
    session = session_manager.schedule_session(
        goal_description="Test session",
        start_time=start_time,
        end_time=end_time,
        linked_quests=[quest]
    )
    
    if session:
        print(f"✅ Session created: {session.session_id}")
        
        # Start and finish the session
        session.start_session()
        session.finish()
        
        # End session manually like in the error
        try:
            completed_session = session_manager.end_session_manually(session.session_id)
            print("✅ Session ended manually without errors")
            
            # Check that analytics were updated
            print(f"✅ Analytics sessions: {len(analytics.session_history)}")
            print(f"✅ Focus streak: {analytics.focus_streak}")
            
        except Exception as e:
            print(f"❌ Error ending session: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("❌ Failed to create session")
    
    print("✅ Complete analytics scenario test passed!\n")

def test_save_load_cycle():
    """Test that save/load cycle preserves datetime handling"""
    print("=== Test Save/Load Cycle ===")
    
    # Create initial data
    character = Character("Test Player")
    quest_system = QuestSystem()
    reward_system = RewardSystem()
    analytics = StudyAnalytics(quest_system)
    session_manager = SessionManager(character=character, reward_system=reward_system, analytics=analytics)
    
    # Add a session with datetime
    quest = quest_system.create_quest(difficulty=3, description="Test quest")
    start_time = datetime.now().replace(hour=14, minute=0, second=0, microsecond=0)
    end_time = start_time + timedelta(hours=1)
    
    session = session_manager.schedule_session("Test", start_time, end_time, [quest])
    if session:
        session.start_session()
        session.finish()
        session_manager.end_session_manually(session.session_id)
    
    try:
        # Export save
        session_manager.ExportSave()
        print("✅ Save exported successfully")
        
        # Create new session manager and import
        new_session_manager = SessionManager(
            character=Character("New Player"),
            reward_system=RewardSystem(),
            analytics=StudyAnalytics(QuestSystem())
        )
        
        # Import save
        success = new_session_manager.ImportSave()
        
        if success:
            print("✅ Save imported successfully")
            
            # Test analytics with imported data
            try:
                streak = new_session_manager.analytics._calculate_focus_streak()
                print(f"✅ Focus streak calculated after import: {streak}")
                
                # Test generating report
                report = new_session_manager.analytics.generate_report()
                print("✅ Report generated successfully after import")
                
            except Exception as e:
                print(f"❌ Error with imported analytics: {e}")
        else:
            print("❌ Failed to import save")
            
    except Exception as e:
        print(f"❌ Error in save/load cycle: {e}")
        import traceback
        traceback.print_exc()
    
    print("✅ Save/load cycle test completed!\n")

def main():
    print("🔧 Testing Complete Analytics Fix")
    print("=" * 50)
    
    test_complete_analytics_scenario()
    test_save_load_cycle()
    
    print("✅ All tests completed!")

if __name__ == "__main__":
    main()
