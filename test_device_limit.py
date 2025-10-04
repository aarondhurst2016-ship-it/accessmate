#!/usr/bin/env python3
"""
Test script for device limit functionality
Tests that accounts can only have 3 devices maximum
"""

import os
import sys
import json
import uuid

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import the functions we need to test
from gui import (
    backend_add_device, 
    backend_remove_device, 
    backend_list_devices, 
    backend_check_device_limit,
    MAX_DEVICES_PER_ACCOUNT,
    BACKEND_FILE
)

def clean_test_data():
    """Clean up test data"""
    if os.path.exists(BACKEND_FILE):
        os.remove(BACKEND_FILE)
    print("🧹 Cleaned test data")

def test_device_limit():
    """Test the 3-device limit functionality"""
    print(f"🧪 Testing device limit functionality (max {MAX_DEVICES_PER_ACCOUNT} devices)")
    
    test_email = "test@example.com"
    
    # Test 1: Add devices up to limit
    print("\n📱 Test 1: Adding devices up to limit")
    for i in range(MAX_DEVICES_PER_ACCOUNT):
        device_id = str(uuid.uuid4())
        device_name = f"Test Device {i+1}"
        result = backend_add_device(test_email, device_id, device_name)
        print(f"  Device {i+1}: {'✅ Added' if result else '❌ Failed'}")
        assert result, f"Should be able to add device {i+1}"
    
    # Verify we have exactly 3 devices
    devices = backend_list_devices(test_email)
    print(f"  📊 Current device count: {len(devices)}")
    assert len(devices) == MAX_DEVICES_PER_ACCOUNT, f"Should have {MAX_DEVICES_PER_ACCOUNT} devices"
    
    # Test 2: Try to add a 4th device (should fail)
    print("\n🚫 Test 2: Trying to add 4th device (should fail)")
    device_4_id = str(uuid.uuid4())
    result = backend_add_device(test_email, device_4_id, "Test Device 4")
    print(f"  4th device: {'❌ Correctly rejected' if not result else '⚠️ Incorrectly allowed'}")
    assert not result, "Should not be able to add 4th device"
    
    # Verify limit check works
    limit_reached = backend_check_device_limit(test_email)
    print(f"  📊 Device limit check: {'✅ Limit reached' if limit_reached else '❌ Not reached'}")
    assert limit_reached, "Device limit should be reached"
    
    # Test 3: Remove a device and add a new one
    print("\n🔄 Test 3: Remove device and add new one")
    devices = backend_list_devices(test_email)
    first_device_id = devices[0]["id"] if isinstance(devices[0], dict) else devices[0]
    
    # Remove first device
    remove_result = backend_remove_device(test_email, first_device_id)
    print(f"  Remove device: {'✅ Removed' if remove_result else '❌ Failed'}")
    assert remove_result, "Should be able to remove device"
    
    # Verify we now have 2 devices
    devices = backend_list_devices(test_email)
    print(f"  📊 Device count after removal: {len(devices)}")
    assert len(devices) == MAX_DEVICES_PER_ACCOUNT - 1, f"Should have {MAX_DEVICES_PER_ACCOUNT - 1} devices"
    
    # Add new device (should work now)
    new_device_id = str(uuid.uuid4())
    add_result = backend_add_device(test_email, new_device_id, "Replacement Device")
    print(f"  Add new device: {'✅ Added' if add_result else '❌ Failed'}")
    assert add_result, "Should be able to add device after removal"
    
    # Verify we're back to 3 devices
    devices = backend_list_devices(test_email)
    print(f"  📊 Final device count: {len(devices)}")
    assert len(devices) == MAX_DEVICES_PER_ACCOUNT, f"Should have {MAX_DEVICES_PER_ACCOUNT} devices again"
    
    print("\n✅ All device limit tests passed!")

def test_duplicate_device():
    """Test that duplicate devices aren't added"""
    print("\n🔁 Test: Duplicate device handling")
    
    test_email = "test2@example.com"
    device_id = str(uuid.uuid4())
    device_name = "Test Device"
    
    # Add device first time
    result1 = backend_add_device(test_email, device_id, device_name)
    print(f"  First add: {'✅ Added' if result1 else '❌ Failed'}")
    assert result1, "Should be able to add device first time"
    
    # Try to add same device again
    result2 = backend_add_device(test_email, device_id, device_name)
    print(f"  Duplicate add: {'✅ Handled correctly' if result2 else '❌ Rejected incorrectly'}")
    assert result2, "Should handle duplicate device gracefully"
    
    # Verify we still only have 1 device
    devices = backend_list_devices(test_email)
    print(f"  📊 Device count: {len(devices)}")
    assert len(devices) == 1, "Should only have 1 device (no duplicates)"
    
    print("✅ Duplicate device test passed!")

if __name__ == "__main__":
    print("🚀 Starting AccessMate Device Limit Tests")
    print(f"📋 Maximum devices per account: {MAX_DEVICES_PER_ACCOUNT}")
    
    try:
        clean_test_data()
        test_device_limit()
        test_duplicate_device()
        print("\n🎉 All tests passed! Device limit functionality is working correctly.")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        clean_test_data()