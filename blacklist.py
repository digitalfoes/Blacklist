"""
Core Blacklist Management Logic
Handles data persistence and basic CRUD operations for the blacklist.
"""
import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path


class BlacklistManager:
    """
    Core blacklist manager that handles data persistence and operations.
    Works in conjunction with CrewAI agents for intelligent management.
    """
    
    def __init__(self, data_file: str = "data/blacklist.json"):
        """
        Initialize the BlacklistManager.
        
        Args:
            data_file: Path to the JSON file storing blacklist data
        """
        self.data_file = data_file
        self._ensure_data_file()
        self.blacklist = self._load_data()
    
    def _ensure_data_file(self):
        """Ensure the data directory and file exist."""
        data_dir = os.path.dirname(self.data_file)
        if data_dir and not os.path.exists(data_dir):
            os.makedirs(data_dir)
        
        if not os.path.exists(self.data_file):
            with open(self.data_file, 'w') as f:
                json.dump({"entries": [], "metadata": {"version": "1.0"}}, f, indent=2)
    
    def _load_data(self) -> Dict:
        """Load blacklist data from file."""
        try:
            with open(self.data_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {"entries": [], "metadata": {"version": "1.0"}}
    
    def _save_data(self):
        """Save blacklist data to file."""
        with open(self.data_file, 'w') as f:
            json.dump(self.blacklist, f, indent=2)
    
    def _generate_id(self) -> str:
        """Generate a unique ID for a new entry."""
        if not self.blacklist.get("entries"):
            return "BL001"
        
        existing_ids = [entry.get("id", "") for entry in self.blacklist["entries"]]
        numeric_ids = [int(id[2:]) for id in existing_ids if id.startswith("BL") and id[2:].isdigit()]
        
        if numeric_ids:
            next_num = max(numeric_ids) + 1
        else:
            next_num = 1
        
        return f"BL{next_num:03d}"
    
    def add_entry(self, name: str, reason: str, threat_level: str = "Medium", 
                  notes: str = "", category: str = "General") -> Dict:
        """
        Add a new entry to the blacklist.
        
        Args:
            name: Name of the entity to blacklist
            reason: Reason for blacklisting
            threat_level: Threat level (Low, Medium, High, Critical)
            notes: Additional notes
            category: Category of the threat
        
        Returns:
            The created entry
        """
        entry = {
            "id": self._generate_id(),
            "name": name,
            "reason": reason,
            "threat_level": threat_level,
            "notes": notes,
            "category": category,
            "date_added": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "status": "active"
        }
        
        self.blacklist["entries"].append(entry)
        self._save_data()
        return entry
    
    def remove_entry(self, identifier: str) -> Optional[Dict]:
        """
        Remove an entry from the blacklist.
        
        Args:
            identifier: ID or name of the entry to remove
        
        Returns:
            The removed entry, or None if not found
        """
        for i, entry in enumerate(self.blacklist["entries"]):
            if entry.get("id") == identifier or entry.get("name").lower() == identifier.lower():
                removed = self.blacklist["entries"].pop(i)
                self._save_data()
                return removed
        
        return None
    
    def update_entry(self, identifier: str, **updates) -> Optional[Dict]:
        """
        Update an existing entry.
        
        Args:
            identifier: ID or name of the entry to update
            **updates: Fields to update
        
        Returns:
            The updated entry, or None if not found
        """
        for entry in self.blacklist["entries"]:
            if entry.get("id") == identifier or entry.get("name").lower() == identifier.lower():
                entry.update(updates)
                entry["last_updated"] = datetime.now().isoformat()
                self._save_data()
                return entry
        
        return None
    
    def get_entry(self, identifier: str) -> Optional[Dict]:
        """
        Get a specific entry by ID or name.
        
        Args:
            identifier: ID or name of the entry
        
        Returns:
            The entry, or None if not found
        """
        for entry in self.blacklist["entries"]:
            if entry.get("id") == identifier or entry.get("name").lower() == identifier.lower():
                return entry
        
        return None
    
    def search_entries(self, query: str = "", threat_level: str = "", 
                      category: str = "") -> List[Dict]:
        """
        Search for entries matching criteria.
        
        Args:
            query: Search query (matches name, reason, notes)
            threat_level: Filter by threat level
            category: Filter by category
        
        Returns:
            List of matching entries
        """
        results = []
        query_lower = query.lower()
        
        for entry in self.blacklist["entries"]:
            # Check query match
            if query:
                searchable_text = f"{entry.get('name', '')} {entry.get('reason', '')} {entry.get('notes', '')}".lower()
                if query_lower not in searchable_text:
                    continue
            
            # Check threat level
            if threat_level and entry.get("threat_level") != threat_level:
                continue
            
            # Check category
            if category and entry.get("category") != category:
                continue
            
            results.append(entry)
        
        return results
    
    def list_all_entries(self, sort_by: str = "threat_level") -> List[Dict]:
        """
        List all entries, optionally sorted.
        
        Args:
            sort_by: Field to sort by (threat_level, date_added, name)
        
        Returns:
            List of all entries
        """
        entries = self.blacklist["entries"].copy()
        
        if sort_by == "threat_level":
            threat_order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
            entries.sort(key=lambda x: threat_order.get(x.get("threat_level", "Medium"), 2))
        elif sort_by == "date_added":
            entries.sort(key=lambda x: x.get("date_added", ""), reverse=True)
        elif sort_by == "name":
            entries.sort(key=lambda x: x.get("name", "").lower())
        
        return entries
    
    def get_statistics(self) -> Dict:
        """
        Get statistics about the blacklist.
        
        Returns:
            Dictionary containing statistics
        """
        total = len(self.blacklist["entries"])
        
        threat_counts = {"Low": 0, "Medium": 0, "High": 0, "Critical": 0}
        category_counts = {}
        
        for entry in self.blacklist["entries"]:
            threat_level = entry.get("threat_level", "Medium")
            threat_counts[threat_level] = threat_counts.get(threat_level, 0) + 1
            
            category = entry.get("category", "General")
            category_counts[category] = category_counts.get(category, 0) + 1
        
        return {
            "total_entries": total,
            "threat_level_breakdown": threat_counts,
            "category_breakdown": category_counts,
            "last_updated": datetime.now().isoformat()
        }
    
    def export_to_file(self, filename: str):
        """
        Export blacklist to a file.
        
        Args:
            filename: Output filename
        """
        with open(filename, 'w') as f:
            json.dump(self.blacklist, f, indent=2)
    
    def import_from_file(self, filename: str):
        """
        Import blacklist from a file.
        
        Args:
            filename: Input filename
        """
        with open(filename, 'r') as f:
            imported_data = json.load(f)
            self.blacklist = imported_data
            self._save_data()
