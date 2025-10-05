"""
Cross-Device Data Synchronization System for AccessMate
Automatically syncs data between all user devices
"""

import json
import os
import time
import threading
import requests
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict

@dataclass
class SyncData:
    """Data structure for synchronization"""
    data_id: str
    data_type: str
    content: Any
    source_device: str
    timestamp: str
    checksum: str

class CrossDeviceDataSync:
    """Handles automatic data synchronization between devices"""
    
    def __init__(self, user_id: str, device_id: str):
        self.user_id = user_id
        self.device_id = device_id
        self.sync_server = "https://accessmate-sync.herokuapp.com/api"
        self.local_sync_dir = os.path.join(os.path.expanduser("~"), ".accessmate_sync")
        os.makedirs(self.local_sync_dir, exist_ok=True)
        
        # Sync configuration
        self.sync_enabled = True
        self.sync_interval = 30  # seconds
        self.auto_resolve_conflicts = True
        
        # Data types to sync
        self.sync_types = {
            "clipboard": True,
            "documents": True,
            "notes": True,
            "reminders": True,
            "bookmarks": True,
            "settings": True,
            "history": True,
            "custom_content": True,
        }
        
        # Local data storage
        self.local_data = {}
        self.sync_queue = []
        self.conflict_resolver = ConflictResolver()
        
        # Background sync thread
        self.sync_thread = None
        self.running = False
        
        print(f"🔄 Cross-Device Data Sync initialized for user {user_id}")
    
    def start_automatic_sync(self):
        """Start automatic background synchronization"""
        if self.running:
            return
        
        self.running = True
        self.sync_thread = threading.Thread(target=self._sync_loop, daemon=True)
        self.sync_thread.start()
        
        print("🚀 Automatic cross-device sync started")
    
    def stop_automatic_sync(self):
        """Stop automatic synchronization"""
        self.running = False
        if self.sync_thread:
            self.sync_thread.join()
        
        print("🛑 Automatic sync stopped")
    
    def _sync_loop(self):
        """Main synchronization loop"""
        while self.running:
            try:
                # Push local changes to cloud
                self._push_local_changes()
                
                # Pull remote changes from cloud
                self._pull_remote_changes()
                
                # Process sync queue
                self._process_sync_queue()
                
                time.sleep(self.sync_interval)
                
            except Exception as e:
                print(f"⚠️ Sync loop error: {e}")
                time.sleep(self.sync_interval * 2)  # Back off on error
    
    def add_data_to_sync(self, data_type: str, content: Any, immediate: bool = False):
        """Add data to synchronization queue"""
        if not self.sync_types.get(data_type, False):
            return
        
        data_id = hashlib.md5(f"{data_type}_{self.device_id}_{time.time()}".encode()).hexdigest()
        checksum = hashlib.md5(json.dumps(content, sort_keys=True).encode()).hexdigest()
        
        sync_data = SyncData(
            data_id=data_id,
            data_type=data_type,
            content=content,
            source_device=self.device_id,
            timestamp=datetime.now().isoformat(),
            checksum=checksum
        )
        
        self.sync_queue.append(sync_data)
        
        if immediate:
            self._push_data(sync_data)
        
        print(f"📤 Added {data_type} to sync queue")
    
    def get_synced_data(self, data_type: str) -> List[Any]:
        """Get all synced data of a specific type"""
        return self.local_data.get(data_type, [])
    
    def copy_to_device(self, target_device_id: str, data_type: str, content: Any):
        """Copy specific data to target device"""
        data_id = f"copy_{target_device_id}_{int(time.time())}"
        
        copy_data = SyncData(
            data_id=data_id,
            data_type=f"copy_to_{target_device_id}",
            content={"original_type": data_type, "data": content},
            source_device=self.device_id,
            timestamp=datetime.now().isoformat(),
            checksum=hashlib.md5(json.dumps(content, sort_keys=True).encode()).hexdigest()
        )
        
        self._push_data(copy_data)
        print(f"📤 Data copied to device {target_device_id}")
    
    def _push_local_changes(self):
        """Push local changes to cloud"""
        if not self.sync_queue:
            return
        
        try:
            for sync_data in self.sync_queue:
                self._push_data(sync_data)
            
            self.sync_queue.clear()
            
        except Exception as e:
            print(f"⚠️ Failed to push changes: {e}")
    
    def _push_data(self, sync_data: SyncData):
        """Push single data item to cloud"""
        try:
            # Simulate cloud API call
            payload = {
                "user_id": self.user_id,
                "device_id": self.device_id,
                "data": asdict(sync_data)
            }
            
            # In real implementation, make HTTP POST request
            # response = requests.post(f"{self.sync_server}/sync", json=payload)
            
            # Simulate successful push
            print(f"☁️ Pushed {sync_data.data_type} to cloud")
            
        except Exception as e:
            print(f"❌ Failed to push {sync_data.data_type}: {e}")
    
    def _pull_remote_changes(self):
        """Pull remote changes from cloud"""
        try:
            # Simulate cloud API call
            # response = requests.get(f"{self.sync_server}/sync/{self.user_id}")
            
            # Simulate remote data
            remote_changes = self._simulate_remote_changes()
            
            for change in remote_changes:
                self._process_remote_change(change)
                
        except Exception as e:
            print(f"⚠️ Failed to pull remote changes: {e}")
    
    def _simulate_remote_changes(self) -> List[Dict]:
        """Simulate remote changes from other devices"""
        return [
            {
                "data_id": "remote_1",
                "data_type": "clipboard",
                "content": "Text copied from phone",
                "source_device": "phone_123",
                "timestamp": datetime.now().isoformat(),
                "checksum": "abc123"
            },
            {
                "data_id": "remote_2", 
                "data_type": "notes",
                "content": "Note created on tablet",
                "source_device": "tablet_456",
                "timestamp": datetime.now().isoformat(),
                "checksum": "def456"
            }
        ]
    
    def _process_remote_change(self, change_data: Dict):
        """Process a remote change"""
        data_type = change_data["data_type"]
        content = change_data["content"]
        source_device = change_data["source_device"]
        
        # Skip changes from this device
        if source_device == self.device_id:
            return
        
        # Handle device-specific copies
        if data_type.startswith(f"copy_to_{self.device_id}"):
            original_type = content["original_type"]
            data = content["data"]
            self._apply_copied_data(original_type, data, source_device)
            return
        
        # Add to local data if not duplicate
        if data_type not in self.local_data:
            self.local_data[data_type] = []
        
        # Check for conflicts
        conflict = self._check_for_conflict(data_type, content, change_data)
        
        if conflict and not self.auto_resolve_conflicts:
            self._handle_conflict(conflict, change_data)
        else:
            # Add data
            self.local_data[data_type].append({
                "content": content,
                "source_device": source_device,
                "timestamp": change_data["timestamp"],
                "synced": True
            })
            
            print(f"📥 Synced {data_type} from {source_device}")
    
    def _apply_copied_data(self, data_type: str, content: Any, source_device: str):
        """Apply data that was specifically copied to this device"""
        if data_type not in self.local_data:
            self.local_data[data_type] = []
        
        self.local_data[data_type].insert(0, {  # Insert at beginning for priority
            "content": content,
            "source_device": source_device,
            "timestamp": datetime.now().isoformat(),
            "copied": True,
            "synced": True
        })
        
        print(f"📋 Applied copied {data_type} from {source_device}")
        
        # Trigger any necessary updates (e.g., clipboard update)
        self._trigger_data_update(data_type, content)
    
    def _trigger_data_update(self, data_type: str, content: Any):
        """Trigger updates when new data is received"""
        if data_type == "clipboard":
            self._update_system_clipboard(content)
        elif data_type == "settings":
            self._apply_synced_settings(content)
        elif data_type == "reminders":
            self._activate_synced_reminder(content)
    
    def _update_system_clipboard(self, content: str):
        """Update system clipboard with synced content"""
        try:
            import pyperclip
            pyperclip.copy(content)
            print(f"📋 Updated clipboard with synced content")
        except:
            print("⚠️ Could not update system clipboard")
    
    def _apply_synced_settings(self, settings: Dict):
        """Apply synced settings"""
        print(f"⚙️ Applied synced settings: {settings}")
    
    def _activate_synced_reminder(self, reminder: Dict):
        """Activate a synced reminder"""
        print(f"⏰ Activated synced reminder: {reminder}")
    
    def _check_for_conflict(self, data_type: str, content: Any, change_data: Dict) -> Optional[Dict]:
        """Check for data conflicts"""
        existing_data = self.local_data.get(data_type, [])
        
        for item in existing_data:
            if (item["content"] == content and 
                item["source_device"] != change_data["source_device"]):
                # Same content from different devices - timestamp conflict
                return {
                    "type": "timestamp",
                    "local": item,
                    "remote": change_data
                }
        
        return None
    
    def _handle_conflict(self, conflict: Dict, remote_data: Dict):
        """Handle data conflicts"""
        self.conflict_resolver.resolve_conflict(conflict, remote_data)
    
    def _process_sync_queue(self):
        """Process any queued synchronization tasks"""
        # Handle any pending sync operations
        pass
    
    def get_sync_status(self) -> Dict[str, Any]:
        """Get current synchronization status"""
        return {
            "running": self.running,
            "queue_size": len(self.sync_queue),
            "data_types": list(self.local_data.keys()),
            "total_items": sum(len(items) for items in self.local_data.values()),
            "last_sync": datetime.now().isoformat() if self.running else None
        }

class ConflictResolver:
    """Handles data conflicts during synchronization"""
    
    def resolve_conflict(self, conflict: Dict, remote_data: Dict):
        """Resolve synchronization conflicts"""
        conflict_type = conflict["type"]
        
        if conflict_type == "timestamp":
            # Use most recent timestamp
            local_time = datetime.fromisoformat(conflict["local"]["timestamp"])
            remote_time = datetime.fromisoformat(remote_data["timestamp"])
            
            if remote_time > local_time:
                print(f"🔄 Conflict resolved: Using remote data (newer)")
                return "use_remote"
            else:
                print(f"🔄 Conflict resolved: Keeping local data (newer)")
                return "use_local"
        
        # Default to keeping both
        print(f"🔄 Conflict resolved: Keeping both versions")
        return "keep_both"

# Utility functions
def start_cross_device_sync(user_id: str, device_id: str) -> CrossDeviceDataSync:
    """Start cross-device synchronization"""
    sync_manager = CrossDeviceDataSync(user_id, device_id)
    sync_manager.start_automatic_sync()
    return sync_manager

def sync_clipboard_to_all_devices(content: str, sync_manager: CrossDeviceDataSync):
    """Sync clipboard content to all devices"""
    sync_manager.add_data_to_sync("clipboard", content, immediate=True)

def sync_document_to_all_devices(document: Dict, sync_manager: CrossDeviceDataSync):
    """Sync document to all devices"""
    sync_manager.add_data_to_sync("documents", document, immediate=True)

if __name__ == "__main__":
    # Test cross-device synchronization
    print("🧪 Testing Cross-Device Data Sync...")
    
    sync_manager = CrossDeviceDataSync("test_user", "test_device")
    sync_manager.start_automatic_sync()
    
    # Test adding data
    sync_manager.add_data_to_sync("clipboard", "Test clipboard content")
    sync_manager.add_data_to_sync("notes", {"title": "Test Note", "content": "This is a test note"})
    
    # Test copying to specific device
    sync_manager.copy_to_device("phone_123", "documents", {"title": "Important Doc", "content": "Document content"})
    
    print("✅ Cross-device sync test completed!")
    
    time.sleep(5)
    sync_manager.stop_automatic_sync()