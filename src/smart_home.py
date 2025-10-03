"""
Smart Home Device Control Module (Initial Architecture)

This module provides the architecture and basic backend for smart home device control.
It is designed to be extended for additional device types and protocols.
"""

import threading
import time


# Supported device types (expanded)
SUPPORTED_DEVICE_TYPES = ["smart_plug", "smart_light", "smart_bulb", "smart_thermostat", "smart_tv"]

# Supported protocols (expanded)
SUPPORTED_PROTOCOLS = ["wifi", "bluetooth"]



class SmartHomeDevice:
    TV_APP_CONTENT_MAP = {
        "YouTube": ["YouTube Originals", "YouTube Movies"],
        "Netflix": ["Stranger Things", "The Crown", "Squid Game"],
        "Disney+": ["The Mandalorian", "Frozen", "Loki"],
        "Prime Video": ["The Boys", "The Marvelous Mrs. Maisel"],
        "Hulu": ["The Handmaid's Tale", "Only Murders in the Building"]
    }

    def __init__(self, name, device_type, protocol, address):
        self.name = name
        self.device_type = device_type
        self.protocol = protocol
        self.address = address
        self.status = "off"
        # TV-specific state
        if device_type == "smart_tv":
            self.volume = 10
            self.muted = False
            self.input_source = "HDMI1"
            self.current_app = None

    def turn_on(self):
        self.status = "on"
        print(f"{self.name} turned ON.")

    def turn_off(self):
        self.status = "off"
        print(f"{self.name} turned OFF.")

    def get_status(self):
        return self.status

    # TV-specific controls
    def set_volume(self, value):
        if self.device_type == "smart_tv":
            self.volume = max(0, min(100, value))
            print(f"{self.name} volume set to {self.volume}")

    def change_input(self, source):
        if self.device_type == "smart_tv":
            self.input_source = source
            print(f"{self.name} input changed to {self.input_source}")

    def mute(self):
        if self.device_type == "smart_tv":
            self.muted = True
            print(f"{self.name} muted")

    def unmute(self):
        if self.device_type == "smart_tv":
            self.muted = False
            print(f"{self.name} unmuted")

    def launch_app(self, app_name):
        if self.device_type == "smart_tv":
            self.current_app = app_name
            print(f"{self.name} launched app: {app_name}")

    def control_app(self, app_name, command):
        if self.device_type == "smart_tv" and self.current_app == app_name:
            print(f"{self.name} sent command '{command}' to app '{app_name}'")

    def play_content(self, title):
        if self.device_type != "smart_tv":
            return
        # Find app for content
        for app, shows in self.TV_APP_CONTENT_MAP.items():
            if title in shows:
                self.launch_app(app)
                print(f"{self.name} is now playing '{title}' on {app}")
                return
        # Default: YouTube
        self.launch_app("YouTube")
        print(f"{self.name} is now searching for '{title}' on YouTube")


class SmartHomeController:
    def __init__(self):
        self.devices = []

    def discover_devices(self):
        # Simulate device discovery (in real implementation, scan network)
        print("Discovering devices...")
        time.sleep(1)
        # Add multiple mock devices for demonstration
        demo_devices = [
            SmartHomeDevice(
                name="Living Room Plug",
                device_type="smart_plug",
                protocol="wifi",
                address="192.168.1.100"
            ),
            SmartHomeDevice(
                name="Bedroom Bulb",
                device_type="smart_bulb",
                protocol="wifi",
                address="192.168.1.101"
            ),
            SmartHomeDevice(
                name="Hallway Light",
                device_type="smart_light",
                protocol="bluetooth",
                address="00:1A:7D:DA:71:13"
            ),
            SmartHomeDevice(
                name="Main Thermostat",
                device_type="smart_thermostat",
                protocol="wifi",
                address="192.168.1.102"
            ),
            SmartHomeDevice(
                name="Family Room TV",
                device_type="smart_tv",
                protocol="wifi",
                address="192.168.1.110"
            )
        ]
        self.devices = demo_devices
        print(f"Discovered: {[d.name for d in demo_devices]}")
        return self.devices

    def add_device(self, device):
        self.devices.append(device)

    def get_devices(self):
        return self.devices


    def control_device(self, device_name, action, **kwargs):
        for device in self.devices:
            if device.name == device_name:
                if action == "on":
                    device.turn_on()
                elif action == "off":
                    device.turn_off()
                elif action == "set_volume" and device.device_type == "smart_tv":
                    device.set_volume(kwargs.get("value", 10))
                elif action == "change_input" and device.device_type == "smart_tv":
                    device.change_input(kwargs.get("source", "HDMI1"))
                elif action == "mute" and device.device_type == "smart_tv":
                    device.mute()
                elif action == "unmute" and device.device_type == "smart_tv":
                    device.unmute()
                elif action == "launch_app" and device.device_type == "smart_tv":
                    device.launch_app(kwargs.get("app_name", "YouTube"))
                elif action == "control_app" and device.device_type == "smart_tv":
                    device.control_app(kwargs.get("app_name", "YouTube"), kwargs.get("command", "play"))
                elif action == "play_content" and device.device_type == "smart_tv":
                    device.play_content(kwargs.get("title", ""))
                return device.get_status()
        return None

# Example usage (for testing, remove in production)
if __name__ == "__main__":
    controller = SmartHomeController()
    controller.discover_devices()
    controller.control_device("Living Room Plug", "on")
    controller.control_device("Living Room Plug", "off")
