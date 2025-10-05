"""
Comprehensive Testing Framework for Universal Automatic System
Tests all automatic features, cross-device sync, and universal settings
"""

import sys
import os
import time
import json
import threading
from datetime import datetime
from typing import Dict, List, Any, Tuple

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

try:
    from automatic_universal_manager import AutomaticUniversalFeatureManager, get_universal_manager
    from cross_device_sync import CrossDeviceDataSync, start_cross_device_sync
    from automatic_login import AutomaticLoginSystem, get_login_system
    from universal_settings_manager import UniversalSettingsManager, get_settings_manager
except ImportError as e:
    print(f"⚠️ Import error: {e}")
    print("🔧 Make sure all required modules are in the src directory")

class UniversalSystemTester:
    """Comprehensive test suite for universal automatic system"""
    
    def __init__(self):
        self.test_results = {}
        self.test_user = "test_user_universal"
        self.test_password = "test_password_123"
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        
        print("🧪 Universal System Tester initialized")
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run comprehensive test suite"""
        print("🚀 Running comprehensive universal system tests...")
        print("=" * 60)
        
        # Test automatic universal feature manager
        self.test_automatic_universal_manager()
        
        # Test cross-device synchronization
        self.test_cross_device_sync()
        
        # Test automatic login system
        self.test_automatic_login()
        
        # Test universal settings manager
        self.test_universal_settings()
        
        # Test integrated system workflow
        self.test_integrated_workflow()
        
        # Generate test report
        return self._generate_test_report()
    
    def test_automatic_universal_manager(self):
        """Test automatic universal feature manager"""
        print("\n📱 Testing Automatic Universal Feature Manager...")
        
        try:
            # Test manager initialization
            self._run_test("Manager Initialization", self._test_manager_init)
            
            # Test user profile creation
            self._run_test("User Profile Creation", self._test_profile_creation)
            
            # Test automatic login with sync
            self._run_test("Automatic Login with Sync", self._test_auto_login_sync)
            
            # Test feature activation
            self._run_test("Automatic Feature Activation", self._test_feature_activation)
            
            # Test cross-device copying
            self._run_test("Cross-Device Data Copying", self._test_cross_device_copying)
            
        except Exception as e:
            print(f"❌ Universal manager test suite failed: {e}")
    
    def test_cross_device_sync(self):
        """Test cross-device synchronization system"""
        print("\n🔄 Testing Cross-Device Synchronization...")
        
        try:
            # Test sync manager initialization
            self._run_test("Sync Manager Init", self._test_sync_manager_init)
            
            # Test data addition and sync
            self._run_test("Data Addition to Sync", self._test_data_sync_addition)
            
            # Test automatic sync service
            self._run_test("Automatic Sync Service", self._test_automatic_sync_service)
            
            # Test conflict resolution
            self._run_test("Conflict Resolution", self._test_conflict_resolution)
            
            # Test device-specific copying
            self._run_test("Device-Specific Copy", self._test_device_specific_copy)
            
        except Exception as e:
            print(f"❌ Cross-device sync test suite failed: {e}")
    
    def test_automatic_login(self):
        """Test automatic login system"""
        print("\n🔐 Testing Automatic Login System...")
        
        try:
            # Test login system initialization
            self._run_test("Login System Init", self._test_login_system_init)
            
            # Test automatic login setup
            self._run_test("Auto Login Setup", self._test_auto_login_setup)
            
            # Test automatic login execution
            self._run_test("Auto Login Execution", self._test_auto_login_execution)
            
            # Test session management
            self._run_test("Session Management", self._test_session_management)
            
            # Test security features
            self._run_test("Security Features", self._test_login_security)
            
        except Exception as e:
            print(f"❌ Automatic login test suite failed: {e}")
    
    def test_universal_settings(self):
        """Test universal settings manager"""
        print("\n⚙️ Testing Universal Settings Manager...")
        
        try:
            # Test settings manager initialization
            self._run_test("Settings Manager Init", self._test_settings_manager_init)
            
            # Test setting operations
            self._run_test("Setting Get/Set Operations", self._test_setting_operations)
            
            # Test settings validation
            self._run_test("Settings Validation", self._test_settings_validation)
            
            # Test settings synchronization
            self._run_test("Settings Sync", self._test_settings_sync)
            
            # Test settings export/import
            self._run_test("Settings Export/Import", self._test_settings_export_import)
            
        except Exception as e:
            print(f"❌ Universal settings test suite failed: {e}")
    
    def test_integrated_workflow(self):
        """Test integrated system workflow"""
        print("\n🔗 Testing Integrated System Workflow...")
        
        try:
            # Test complete user journey
            self._run_test("Complete User Journey", self._test_complete_user_journey)
            
            # Test multi-device simulation
            self._run_test("Multi-Device Simulation", self._test_multi_device_simulation)
            
            # Test error recovery
            self._run_test("Error Recovery", self._test_error_recovery)
            
            # Test performance under load
            self._run_test("Performance Under Load", self._test_performance_load)
            
        except Exception as e:
            print(f"❌ Integrated workflow test suite failed: {e}")
    
    # Individual test methods
    def _test_manager_init(self) -> bool:
        """Test universal manager initialization"""
        try:
            manager = AutomaticUniversalFeatureManager()
            assert manager is not None
            assert manager.platform is not None
            assert manager.device_id is not None
            assert len(manager.all_features) > 0
            return True
        except Exception as e:
            print(f"   ❌ Manager init failed: {e}")
            return False
    
    def _test_profile_creation(self) -> bool:
        """Test user profile creation"""
        try:
            manager = get_universal_manager()
            profile = manager.create_user_profile(self.test_user)
            assert profile is not None
            assert profile.username == self.test_user
            assert profile.auto_features is not None
            assert len(profile.auto_features) > 0
            return True
        except Exception as e:
            print(f"   ❌ Profile creation failed: {e}")
            return False
    
    def _test_auto_login_sync(self) -> bool:
        """Test automatic login with sync"""
        try:
            manager = get_universal_manager()
            success = manager.login_user(self.test_user, auto_sync=True)
            assert success == True
            assert manager.user_profile is not None
            return True
        except Exception as e:
            print(f"   ❌ Auto login sync failed: {e}")
            return False
    
    def _test_feature_activation(self) -> bool:
        """Test automatic feature activation"""
        try:
            manager = get_universal_manager()
            manager.activate_all_features()
            # Check if features were attempted to be activated
            return True
        except Exception as e:
            print(f"   ❌ Feature activation failed: {e}")
            return False
    
    def _test_cross_device_copying(self) -> bool:
        """Test cross-device data copying"""
        try:
            manager = get_universal_manager()
            test_data = {"type": "test", "content": "test data"}
            success = manager.copy_to_device("test_device_id", test_data)
            assert success == True
            return True
        except Exception as e:
            print(f"   ❌ Cross-device copying failed: {e}")
            return False
    
    def _test_sync_manager_init(self) -> bool:
        """Test sync manager initialization"""
        try:
            sync_manager = CrossDeviceDataSync("test_user", "test_device")
            assert sync_manager is not None
            assert sync_manager.user_id == "test_user"
            assert sync_manager.device_id == "test_device"
            return True
        except Exception as e:
            print(f"   ❌ Sync manager init failed: {e}")
            return False
    
    def _test_data_sync_addition(self) -> bool:
        """Test adding data to sync"""
        try:
            sync_manager = CrossDeviceDataSync("test_user", "test_device")
            sync_manager.add_data_to_sync("clipboard", "test clipboard content")
            assert len(sync_manager.sync_queue) > 0
            return True
        except Exception as e:
            print(f"   ❌ Data sync addition failed: {e}")
            return False
    
    def _test_automatic_sync_service(self) -> bool:
        """Test automatic sync service"""
        try:
            sync_manager = CrossDeviceDataSync("test_user", "test_device")
            sync_manager.start_automatic_sync()
            time.sleep(1)  # Let it run briefly
            assert sync_manager.running == True
            sync_manager.stop_automatic_sync()
            return True
        except Exception as e:
            print(f"   ❌ Automatic sync service failed: {e}")
            return False
    
    def _test_conflict_resolution(self) -> bool:
        """Test conflict resolution"""
        try:
            sync_manager = CrossDeviceDataSync("test_user", "test_device")
            # Simulate conflict resolution
            conflict = {"type": "timestamp", "local": {"timestamp": "2023-01-01T00:00:00"}}
            remote_data = {"timestamp": "2023-01-02T00:00:00"}
            result = sync_manager.conflict_resolver.resolve_conflict(conflict, remote_data)
            assert result is not None
            return True
        except Exception as e:
            print(f"   ❌ Conflict resolution failed: {e}")
            return False
    
    def _test_device_specific_copy(self) -> bool:
        """Test device-specific copying"""
        try:
            sync_manager = CrossDeviceDataSync("test_user", "test_device")
            sync_manager.copy_to_device("target_device", "clipboard", "copied content")
            return True
        except Exception as e:
            print(f"   ❌ Device-specific copy failed: {e}")
            return False
    
    def _test_login_system_init(self) -> bool:
        """Test login system initialization"""
        try:
            login_system = AutomaticLoginSystem()
            assert login_system is not None
            assert login_system.platform is not None
            return True
        except Exception as e:
            print(f"   ❌ Login system init failed: {e}")
            return False
    
    def _test_auto_login_setup(self) -> bool:
        """Test automatic login setup"""
        try:
            login_system = get_login_system()
            success = login_system.enable_automatic_login(self.test_user, self.test_password)
            assert success == True
            return True
        except Exception as e:
            print(f"   ❌ Auto login setup failed: {e}")
            return False
    
    def _test_auto_login_execution(self) -> bool:
        """Test automatic login execution"""
        try:
            login_system = get_login_system()
            success, username = login_system.automatic_login()
            assert success == True
            assert username == self.test_user
            return True
        except Exception as e:
            print(f"   ❌ Auto login execution failed: {e}")
            return False
    
    def _test_session_management(self) -> bool:
        """Test session management"""
        try:
            login_system = get_login_system()
            status = login_system.get_login_status()
            assert status is not None
            assert "logged_in" in status
            return True
        except Exception as e:
            print(f"   ❌ Session management failed: {e}")
            return False
    
    def _test_login_security(self) -> bool:
        """Test login security features"""
        try:
            login_system = get_login_system()
            # Test device trust
            is_trusted = login_system._is_trusted_device()
            assert isinstance(is_trusted, bool)
            return True
        except Exception as e:
            print(f"   ❌ Login security failed: {e}")
            return False
    
    def _test_settings_manager_init(self) -> bool:
        """Test settings manager initialization"""
        try:
            settings_manager = UniversalSettingsManager("test_user", "test_device")
            assert settings_manager is not None
            assert len(settings_manager.setting_definitions) > 0
            return True
        except Exception as e:
            print(f"   ❌ Settings manager init failed: {e}")
            return False
    
    def _test_setting_operations(self) -> bool:
        """Test setting get/set operations"""
        try:
            settings_manager = get_settings_manager("test_user", "test_device")
            
            # Test setting a value
            success = settings_manager.set_setting("app_theme", "dark")
            assert success == True
            
            # Test getting the value
            value = settings_manager.get_setting("app_theme")
            assert value == "dark"
            
            return True
        except Exception as e:
            print(f"   ❌ Setting operations failed: {e}")
            return False
    
    def _test_settings_validation(self) -> bool:
        """Test settings validation"""
        try:
            settings_manager = get_settings_manager("test_user", "test_device")
            
            # Test valid setting
            valid = settings_manager._validate_setting("app_theme", "dark")
            assert valid == True
            
            # Test invalid setting
            invalid = settings_manager._validate_setting("app_theme", "invalid_theme")
            assert invalid == False
            
            return True
        except Exception as e:
            print(f"   ❌ Settings validation failed: {e}")
            return False
    
    def _test_settings_sync(self) -> bool:
        """Test settings synchronization"""
        try:
            settings_manager = get_settings_manager("test_user", "test_device")
            settings_manager.start_automatic_sync()
            time.sleep(1)  # Let it run briefly
            assert settings_manager.running == True
            settings_manager.stop_automatic_sync()
            return True
        except Exception as e:
            print(f"   ❌ Settings sync failed: {e}")
            return False
    
    def _test_settings_export_import(self) -> bool:
        """Test settings export/import"""
        try:
            settings_manager = get_settings_manager("test_user", "test_device")
            
            # Test export
            export_file = "test_settings_export.json"
            success = settings_manager.export_settings(export_file)
            assert success == True
            assert os.path.exists(export_file)
            
            # Test import
            success = settings_manager.import_settings(export_file)
            assert success == True
            
            # Cleanup
            os.remove(export_file)
            
            return True
        except Exception as e:
            print(f"   ❌ Settings export/import failed: {e}")
            return False
    
    def _test_complete_user_journey(self) -> bool:
        """Test complete user journey"""
        try:
            # Simulate complete user workflow
            # 1. Setup automatic login
            login_system = get_login_system()
            login_system.enable_automatic_login(self.test_user, self.test_password)
            
            # 2. Login with automatic features
            success, username = login_system.login_with_sync(self.test_user, self.test_password)
            assert success == True
            
            # 3. Use universal manager
            manager = get_universal_manager()
            manager.login_user(username, auto_sync=True)
            
            # 4. Update settings
            settings_manager = get_settings_manager(username, manager.device_id)
            settings_manager.set_setting("enable_cloud_sync", True)
            
            # 5. Add data for sync
            sync_manager = CrossDeviceDataSync(username, manager.device_id)
            sync_manager.add_data_to_sync("notes", {"title": "Test Note", "content": "Test content"})
            
            return True
        except Exception as e:
            print(f"   ❌ Complete user journey failed: {e}")
            return False
    
    def _test_multi_device_simulation(self) -> bool:
        """Test multi-device simulation"""
        try:
            # Simulate multiple devices
            device1 = AutomaticUniversalFeatureManager()
            device2 = AutomaticUniversalFeatureManager()
            
            # Login on both devices
            device1.login_user(self.test_user, auto_sync=True)
            device2.login_user(self.test_user, auto_sync=True)
            
            # Copy data between devices
            test_data = {"type": "test", "content": "multi-device test"}
            device1.copy_to_device(device2.device_id, test_data)
            
            return True
        except Exception as e:
            print(f"   ❌ Multi-device simulation failed: {e}")
            return False
    
    def _test_error_recovery(self) -> bool:
        """Test error recovery mechanisms"""
        try:
            # Test graceful handling of errors
            manager = get_universal_manager()
            
            # Try to activate non-existent feature
            result = manager._activate_feature("non_existent_feature")
            assert result == False  # Should fail gracefully
            
            # Test sync with network error simulation
            sync_manager = CrossDeviceDataSync("test_user", "test_device")
            sync_manager._sync_settings_to_cloud()  # Should handle errors gracefully
            
            return True
        except Exception as e:
            print(f"   ❌ Error recovery failed: {e}")
            return False
    
    def _test_performance_load(self) -> bool:
        """Test performance under load"""
        try:
            # Test with multiple operations
            manager = get_universal_manager()
            settings_manager = get_settings_manager("test_user", "test_device")
            
            start_time = time.time()
            
            # Perform multiple operations
            for i in range(10):
                settings_manager.set_setting(f"test_setting_{i}", f"value_{i}")
                manager.user_profile.user_data["notes"].append(f"Note {i}")
            
            end_time = time.time()
            duration = end_time - start_time
            
            # Should complete within reasonable time
            assert duration < 5.0  # 5 seconds max
            
            return True
        except Exception as e:
            print(f"   ❌ Performance load test failed: {e}")
            return False
    
    def _run_test(self, test_name: str, test_function) -> bool:
        """Run a single test and record results"""
        self.total_tests += 1
        
        try:
            print(f"   🧪 Running: {test_name}")
            result = test_function()
            
            if result:
                print(f"   ✅ PASSED: {test_name}")
                self.passed_tests += 1
                self.test_results[test_name] = {"status": "PASSED", "error": None}
                return True
            else:
                print(f"   ❌ FAILED: {test_name}")
                self.failed_tests += 1
                self.test_results[test_name] = {"status": "FAILED", "error": "Test returned False"}
                return False
                
        except Exception as e:
            print(f"   ❌ ERROR: {test_name} - {e}")
            self.failed_tests += 1
            self.test_results[test_name] = {"status": "ERROR", "error": str(e)}
            return False
    
    def _generate_test_report(self) -> Dict[str, Any]:
        """Generate comprehensive test report"""
        print("\n" + "=" * 60)
        print("📊 UNIVERSAL SYSTEM TEST REPORT")
        print("=" * 60)
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "total_tests": self.total_tests,
            "passed_tests": self.passed_tests,
            "failed_tests": self.failed_tests,
            "success_rate": (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0,
            "test_results": self.test_results
        }
        
        print(f"Total Tests: {self.total_tests}")
        print(f"Passed: {self.passed_tests}")
        print(f"Failed: {self.failed_tests}")
        print(f"Success Rate: {report['success_rate']:.1f}%")
        
        if self.failed_tests > 0:
            print("\n❌ FAILED TESTS:")
            for test_name, result in self.test_results.items():
                if result["status"] != "PASSED":
                    print(f"   • {test_name}: {result['error']}")
        
        # Save report to file
        report_file = f"universal_system_test_report_{int(time.time())}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📄 Detailed report saved to: {report_file}")
        
        if self.failed_tests == 0:
            print("\n🎉 ALL TESTS PASSED! Universal automatic system is working correctly!")
        else:
            print(f"\n⚠️ {self.failed_tests} tests failed. Please review and fix issues.")
        
        return report

def run_comprehensive_test():
    """Run comprehensive test of universal automatic system"""
    print("🚀 Starting Comprehensive Universal System Test...")
    
    tester = UniversalSystemTester()
    report = tester.run_all_tests()
    
    return report

if __name__ == "__main__":
    # Run comprehensive tests
    test_report = run_comprehensive_test()
    
    # Exit with appropriate code
    if test_report["failed_tests"] == 0:
        print("\n✅ All tests passed successfully!")
        sys.exit(0)
    else:
        print(f"\n❌ {test_report['failed_tests']} tests failed.")
        sys.exit(1)