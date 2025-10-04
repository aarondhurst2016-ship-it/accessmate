#!/usr/bin/env python3
"""
Final comprehensive test for device limit and account features
"""

import os
import sys
import json

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from gui import (
    backend_add_device, 
    backend_remove_device, 
    backend_list_devices, 
    backend_mark_purchased,
    backend_check_purchased,
    backend_trial_status,
    MAX_DEVICES_PER_ACCOUNT,
    BACKEND_FILE
)

def test_complete_workflow():
    """Test the complete user workflow with device limits"""
    print("🔄 Testing complete user workflow")
    
    # Clean slate
    if os.path.exists(BACKEND_FILE):
        os.remove(BACKEND_FILE)
    
    test_email = "user@accessmate.com"
    
    # 1. User creates account and logs in on 3 devices
    print("\n📱 Step 1: User logs in on 3 devices")
    for i in range(3):
        device_id = f"device-{i+1}"
        device_name = f"Device {i+1}"
        result = backend_add_device(test_email, device_id, device_name)
        print(f"  Device {i+1}: {'✅' if result else '❌'}")
    
    devices = backend_list_devices(test_email)
    print(f"  📊 Total devices: {len(devices)}/{MAX_DEVICES_PER_ACCOUNT}")
    
    # 2. User tries to log in on 4th device (should be blocked)
    print("\n🚫 Step 2: User tries 4th device")
    result = backend_add_device(test_email, "device-4", "Device 4")
    print(f"  4th device blocked: {'✅' if not result else '❌'}")
    
    # 3. User purchases the app
    print("\n💳 Step 3: User purchases the app")
    backend_mark_purchased(test_email)
    purchased = backend_check_purchased(test_email)
    print(f"  Purchase successful: {'✅' if purchased else '❌'}")
    
    # 4. User removes old device and adds new one
    print("\n🔄 Step 4: Remove old device, add new one")
    devices = backend_list_devices(test_email)
    old_device = devices[0]["id"]
    
    removed = backend_remove_device(test_email, old_device)
    print(f"  Old device removed: {'✅' if removed else '❌'}")
    
    added = backend_add_device(test_email, "device-new", "New Device")
    print(f"  New device added: {'✅' if added else '❌'}")
    
    # 5. Verify final state
    final_devices = backend_list_devices(test_email)
    still_purchased = backend_check_purchased(test_email)
    
    print(f"\n📊 Final state:")
    print(f"  Devices: {len(final_devices)}/{MAX_DEVICES_PER_ACCOUNT}")
    print(f"  Still purchased: {'✅' if still_purchased else '❌'}")
    
    # Verify correct behavior
    assert len(final_devices) == MAX_DEVICES_PER_ACCOUNT
    assert still_purchased
    assert "device-new" in [d["id"] for d in final_devices]
    assert old_device not in [d["id"] for d in final_devices]
    
    print("✅ Complete workflow test passed!")

if __name__ == "__main__":
    print("🚀 Running comprehensive device limit test")
    try:
        test_complete_workflow()
        print("\n🎉 All comprehensive tests passed!")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Clean up
        if os.path.exists(BACKEND_FILE):
            os.remove(BACKEND_FILE)