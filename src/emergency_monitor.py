"""
emergency_monitor.py - Medical emergency detection and response
- Monitors for emergency events (fall, abnormal heart rate, etc.)
- Contacts emergency contacts automatically
- Smart watch integration (plugin system)
"""
import time
import threading
from emergency_contacts import contact_emergency_contacts
from watch_plugins import get_available_plugins, SmartWatchPlugin

# Emergency detection logic
class EmergencyMonitor:
    def __init__(self, plugins, heart_rate_low=40, heart_rate_high=160):
        self.plugins = plugins  # List of SmartWatchPlugin
        self.heart_rate_low = heart_rate_low
        self.heart_rate_high = heart_rate_high
        self.monitoring = False
        self.last_alert = 0
        self.alert_interval = 60  # seconds

    def start(self):
        self.monitoring = True
        threading.Thread(target=self.monitor_loop, daemon=True).start()

    def stop(self):
        self.monitoring = False

    def monitor_loop(self):
        while self.monitoring:
            for plugin in self.plugins:
                if not plugin.is_connected():
                    continue
                hr = plugin.get_heart_rate()
                fall = plugin.check_fall()
                now = time.time()
                if (hr is not None and (hr < self.heart_rate_low or hr > self.heart_rate_high) or fall) and (now - self.last_alert > self.alert_interval):
                    print(f"Medical emergency detected by {plugin.get_name()}!")
                    contact_emergency_contacts(reason=f"Medical emergency detected by {plugin.get_name()}.")
                    self.last_alert = now
            time.sleep(2)

if __name__ == "__main__":
    plugins = get_available_plugins()
    monitor = EmergencyMonitor(plugins)
    print("Starting emergency monitor (multi-watch plugin). Press Ctrl+C to stop.")
    monitor.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping monitor.")
        monitor.stop()
