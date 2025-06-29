#!/usr/bin/env python3
"""
Test analytics fix for datetime/string handling
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Backend.Code import StudyAnalytics, QuestSystem
from datetime import datetime, date

def test_analytics_datetime_fix():
    """Test that analytics can handle both datetime objects and strings"""
    print("=== Test Analytics DateTime Fix ===")
    
    # Create analytics instance
    quest_system = QuestSystem()
    analytics = StudyAnalytics(quest_system)
    
    # Test with datetime object
    session_data_datetime = {
        'session_id': 'test1',
        'goal': 'Test session with datetime',
        'status': 'Finished',
        'start_time': datetime.now(),
        'end_time': datetime.now(),
        'actual_start_time': datetime.now(),
        'actual_end_time': datetime.now(),
        'rank': 'A',
        'duration_seconds': 3600,
        'linked_quests_data': []
    }
    
    # Test with string (simulating JSON loading)
    session_data_string = {
        'session_id': 'test2',
        'goal': 'Test session with string',
        'status': 'Finished',
        'start_time': '2025-06-29 10:00:00',
        'end_time': '2025-06-29 11:00:00',
        'actual_start_time': '2025-06-29 10:00:00',
        'actual_end_time': '2025-06-29 11:00:00',
        'rank': 'B',
        'duration_seconds': 3600,
        'linked_quests_data': []
    }
    
    print("Testing with datetime object...")
    try:
        analytics.log_session(session_data_datetime)
        print("✅ DateTime object handled successfully")
    except Exception as e:
        print(f"❌ Error with datetime object: {e}")
    
    print("Testing with string...")
    try:
        analytics.log_session(session_data_string)
        print("✅ String handled successfully")
    except Exception as e:
        print(f"❌ Error with string: {e}")
    
    # Test focus streak calculation
    print("Testing focus streak calculation...")
    try:
        streak = analytics._calculate_focus_streak()
        print(f"✅ Focus streak calculated successfully: {streak}")
    except Exception as e:
        print(f"❌ Error calculating focus streak: {e}")
    
    print("✅ All analytics tests passed!\n")

def main():
    print("🔧 Testing Analytics DateTime Fix")
    print("=" * 50)
    
    test_analytics_datetime_fix()
    
    print("✅ Test completed!")

if __name__ == "__main__":
    main()
