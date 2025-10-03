#!/usr/bin/env python3
"""
AccessMate Battery Status Monitor
Provides voice notifications about device battery level and charging status
Helpful for accessibility users who may not easily see battery indicators
"""

import sys
import platform
import subprocess
import time
from datetime import datetime

class BatteryMonitor:
    def __init__(self):
        self.system = platform.system()
        self.last_announced_level = None
        self.low_battery_threshold = 20
        self.critical_battery_threshold = 10
        
    def get_battery_info(self):
        """Get battery information based on the operating system"""
        try:
            if self.system == "Windows":
                return self._get_windows_battery()
            elif self.system == "Darwin":  # macOS
                return self._get_macos_battery()
            elif self.system == "Linux":
                return self._get_linux_battery()
            else:
                return {"level": None, "charging": None, "error": "Unsupported OS"}
        except Exception as e:
            return {"level": None, "charging": None, "error": str(e)}
    
    def _get_windows_battery(self):
        """Get battery info on Windows using WMIC"""
        try:
            # Get battery level
            result = subprocess.run(
                ["wmic", "path", "win32_battery", "get", "estimatedchargeremaining", "/value"],
                capture_output=True, text=True, shell=True
            )
            level_lines = [line for line in result.stdout.split('\n') if 'EstimatedChargeRemaining' in line]
            level = int(level_lines[0].split('=')[1]) if level_lines else None
            
            # Get charging status
            result = subprocess.run(
                ["wmic", "path", "win32_battery", "get", "batterystatus", "/value"],
                capture_output=True, text=True, shell=True
            )
            status_lines = [line for line in result.stdout.split('\n') if 'BatteryStatus' in line]
            status = int(status_lines[0].split('=')[1]) if status_lines else None
            
            # Battery status codes: 1=Other, 2=Unknown, 3=Fully Charged, 4=Low, 5=Critical, 6=Charging
            charging = status in [6] if status else None
            
            return {"level": level, "charging": charging, "error": None}
        except Exception as e:
            return {"level": None, "charging": None, "error": str(e)}
    
    def _get_macos_battery(self):
        """Get battery info on macOS using pmset"""
        try:
            result = subprocess.run(["pmset", "-g", "batt"], capture_output=True, text=True)
            output = result.stdout
            
            # Parse battery level
            level = None
            charging = None
            
            for line in output.split('\n'):
                if '%' in line:
                    # Extract percentage
                    parts = line.split()
                    for part in parts:
                        if '%' in part:
                            level = int(part.replace('%', '').replace(';', ''))
                            break
                    
                    # Check if charging
                    charging = 'AC Power' in line or 'charging' in line.lower()
                    break
            
            return {"level": level, "charging": charging, "error": None}
        except Exception as e:
            return {"level": None, "charging": None, "error": str(e)}
    
    def _get_linux_battery(self):
        """Get battery info on Linux using /sys/class/power_supply"""
        try:
            import os
            
            battery_path = "/sys/class/power_supply/BAT0"
            if not os.path.exists(battery_path):
                # Try BAT1
                battery_path = "/sys/class/power_supply/BAT1"
                if not os.path.exists(battery_path):
                    return {"level": None, "charging": None, "error": "No battery found"}
            
            # Read battery level
            with open(f"{battery_path}/capacity", 'r') as f:
                level = int(f.read().strip())
            
            # Read charging status
            with open(f"{battery_path}/status", 'r') as f:
                status = f.read().strip().lower()
                charging = status in ['charging', 'full']
            
            return {"level": level, "charging": charging, "error": None}
        except Exception as e:
            return {"level": None, "charging": None, "error": str(e)}
    
    def get_battery_status_message(self):
        """Get a human-readable battery status message"""
        info = self.get_battery_info()
        
        if info["error"]:
            return f"Battery information unavailable: {info['error']}"
        
        if info["level"] is None:
            return "Battery level unknown"
        
        level = info["level"]
        charging = info["charging"]
        
        # Create status message
        message = f"Battery at {level} percent"
        
        if charging:
            message += ", charging"
        else:
            message += ", not charging"
        
        # Add status alerts
        if level <= self.critical_battery_threshold:
            message += " - CRITICAL! Please charge immediately"
        elif level <= self.low_battery_threshold:
            message += " - Low battery warning"
        elif level >= 95:
            message += " - Nearly full"
        
        return message
    
    def should_announce_battery_level(self, current_level):
        """Determine if battery level should be announced"""
        if current_level is None:
            return False
        
        # Always announce critical and low battery
        if current_level <= self.critical_battery_threshold:
            return True
        
        if current_level <= self.low_battery_threshold:
            return True
        
        # Announce every 25% change for normal levels
        if self.last_announced_level is None:
            return True
        
        level_change = abs(current_level - self.last_announced_level)
        return level_change >= 25
    
    def announce_battery_status(self, tts_engine=None):
        """Announce battery status using text-to-speech"""
        message = self.get_battery_status_message()
        
        if tts_engine:
            try:
                tts_engine.say(message)
                tts_engine.runAndWait()
            except:
                print(f"[BATTERY] {message}")
        else:
            print(f"[BATTERY] {message}")
        
        # Update last announced level
        info = self.get_battery_info()
        if info["level"]:
            self.last_announced_level = info["level"]
        
        return message
    
    def start_monitoring(self, check_interval=300, tts_engine=None):
        """Start continuous battery monitoring (interval in seconds)"""
        print(f"[BATTERY MONITOR] Starting battery monitoring (checking every {check_interval//60} minutes)")
        
        try:
            while True:
                info = self.get_battery_info()
                
                if info["level"] is not None:
                    if self.should_announce_battery_level(info["level"]):
                        self.announce_battery_status(tts_engine)
                
                time.sleep(check_interval)
                
        except KeyboardInterrupt:
            print("[BATTERY MONITOR] Monitoring stopped")

def main():
    """Main function for testing battery monitor"""
    battery_monitor = BatteryMonitor()
    
    # Test battery status
    print("=== AccessMate Battery Monitor Test ===")
    message = battery_monitor.announce_battery_status()
    
    # Display detailed info
    info = battery_monitor.get_battery_info()
    print(f"\nDetailed Info:")
    print(f"  System: {battery_monitor.system}")
    print(f"  Level: {info['level']}%")
    print(f"  Charging: {info['charging']}")
    print(f"  Error: {info['error']}")
    
    print(f"\nStatus Message: {message}")

if __name__ == "__main__":
    main()