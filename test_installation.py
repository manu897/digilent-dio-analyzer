#!/usr/bin/env python3
"""
Test script for Digilent DIO Analyzer
Run this to verify the installation and basic functionality
"""

import sys
import os
import time

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test if all modules can be imported"""
    print("Testing imports...")
    
    try:
        from dio_reader import DIOReader
        print("✅ DIOReader imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import DIOReader: {e}")
        return False
    
    try:
        from heap_monitor import HeapMonitor
        print("✅ HeapMonitor imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import HeapMonitor: {e}")
        return False
    
    try:
        from utils import log_event, analyze_toggle_pattern
        print("✅ Utils imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import utils: {e}")
        return False
    
    return True

def test_dio_reader():
    """Test DIOReader functionality"""
    print("\nTesting DIOReader...")
    
    try:
        from dio_reader import DIOReader
        
        dio = DIOReader(pin=0)
        dio.start_reading()
        
        # Test reading for a short time
        for i in range(5):
            state = dio.get_pin_state()
            toggle = dio.check_toggle()
            print(f"  Pin state: {state}, Toggle: {toggle}")
            time.sleep(0.1)
        
        dio.stop_reading()
        print("✅ DIOReader test passed")
        return True
        
    except Exception as e:
        print(f"❌ DIOReader test failed: {e}")
        return False

def test_heap_monitor():
    """Test HeapMonitor functionality"""
    print("\nTesting HeapMonitor...")
    
    try:
        from heap_monitor import HeapMonitor
        
        monitor = HeapMonitor()
        
        # Test memory reading
        memory_info = monitor.get_memory_info()
        if memory_info:
            print(f"  Memory info: RSS={memory_info['rss']//1024//1024}MB, "
                  f"VMS={memory_info['vms']//1024//1024}MB")
        
        # Test logging
        monitor.log_heap_size()
        
        print("✅ HeapMonitor test passed")
        return True
        
    except Exception as e:
        print(f"❌ HeapMonitor test failed: {e}")
        return False

def test_utils():
    """Test utility functions"""
    print("\nTesting utils...")
    
    try:
        from utils import log_event, analyze_toggle_pattern, format_time
        
        # Test logging
        log_event("Test log message")
        
        # Test time formatting
        formatted = format_time(time.time())
        print(f"  Formatted time: {formatted}")
        
        # Test toggle analysis
        test_toggles = [1.0, 1.01, 1.02, 1.03, 1.04, 1.05]
        analysis = analyze_toggle_pattern(test_toggles)
        print(f"  Toggle analysis: {analysis['frequency']:.1f} Hz")
        
        print("✅ Utils test passed")
        return True
        
    except Exception as e:
        print(f"❌ Utils test failed: {e}")
        return False

def test_main_integration():
    """Test main module integration"""
    print("\nTesting main integration...")
    
    try:
        # Import main module
        sys.path.insert(0, 'src')
        from main import DIOAnalyzer
        
        # Create analyzer but don't start monitoring
        analyzer = DIOAnalyzer(pin=0, rapid_toggle_count=3, rapid_window_ms=100)
        
        print("✅ Main integration test passed")
        return True
        
    except Exception as e:
        print(f"❌ Main integration test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Running Digilent DIO Analyzer Tests")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_dio_reader,
        test_heap_monitor,
        test_utils,
        test_main_integration
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
            failed += 1
    
    print(f"\n📊 Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed! The system is ready to use.")
    else:
        print("⚠️  Some tests failed. Please check the installation.")
        sys.exit(1)

if __name__ == "__main__":
    main()
