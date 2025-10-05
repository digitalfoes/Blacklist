"""
Simple Blacklist Management Tool (No API Key Required)
Direct interface to the blacklist manager without AI agents.
"""
import os
from blacklist import BlacklistManager


def print_banner():
    """Print the application banner."""
    print("\n" + "="*60)
    print("  BLACKLIST MANAGEMENT TOOL - Simple Mode")
    print("="*60 + "\n")


def print_menu():
    """Print the main menu."""
    print("\n--- MAIN MENU ---")
    print("1. Add new blacklist entry")
    print("2. Remove entry")
    print("3. Search entries")
    print("4. Update entry")
    print("5. List all entries")
    print("6. View statistics")
    print("7. Export blacklist")
    print("8. Import blacklist")
    print("0. Exit")
    print("-" * 40)


def add_entry_interactive(manager: BlacklistManager):
    """Interactive function to add a new entry."""
    print("\n--- ADD NEW ENTRY ---")
    name = input("Name: ").strip()
    if not name:
        print("❌ Name is required!")
        return
    
    reason = input("Reason for blacklisting: ").strip()
    if not reason:
        print("❌ Reason is required!")
        return
    
    print("\nThreat Levels: Low, Medium, High, Critical")
    threat_level = input("Threat level (default: Medium): ").strip() or "Medium"
    
    category = input("Category (default: General): ").strip() or "General"
    notes = input("Additional notes (optional): ").strip()
    
    try:
        entry = manager.add_entry(name, reason, threat_level, notes, category)
        print(f"\n✅ Entry added successfully!")
        print(f"ID: {entry['id']}")
        print(f"Name: {entry['name']}")
        print(f"Threat Level: {entry['threat_level']}")
        print(f"Date Added: {entry['date_added']}")
    except Exception as e:
        print(f"❌ Error adding entry: {e}")


def remove_entry_interactive(manager: BlacklistManager):
    """Interactive function to remove an entry."""
    print("\n--- REMOVE ENTRY ---")
    identifier = input("Enter entry ID or name: ").strip()
    if not identifier:
        print("❌ Identifier is required!")
        return
    
    try:
        removed = manager.remove_entry(identifier)
        if removed:
            print(f"\n✅ Entry removed successfully!")
            print(f"Removed: {removed['name']} (ID: {removed['id']})")
        else:
            print("❌ Entry not found!")
    except Exception as e:
        print(f"❌ Error removing entry: {e}")


def search_entries_interactive(manager: BlacklistManager):
    """Interactive function to search entries."""
    print("\n--- SEARCH ENTRIES ---")
    query = input("Search query (name, reason, notes): ").strip()
    threat_level = input("Filter by threat level (optional): ").strip()
    category = input("Filter by category (optional): ").strip()
    
    try:
        results = manager.search_entries(query, threat_level, category)
        if results:
            print(f"\n✅ Found {len(results)} entries:")
            for entry in results:
                print(f"\n  ID: {entry['id']}")
                print(f"  Name: {entry['name']}")
                print(f"  Threat Level: {entry['threat_level']}")
                print(f"  Reason: {entry['reason'][:50]}...")
                print(f"  Date Added: {entry['date_added']}")
        else:
            print("❌ No entries found matching your criteria.")
    except Exception as e:
        print(f"❌ Error searching: {e}")


def update_entry_interactive(manager: BlacklistManager):
    """Interactive function to update an entry."""
    print("\n--- UPDATE ENTRY ---")
    identifier = input("Enter entry ID or name: ").strip()
    if not identifier:
        print("❌ Identifier is required!")
        return
    
    # Check if entry exists
    entry = manager.get_entry(identifier)
    if not entry:
        print("❌ Entry not found!")
        return
    
    print(f"\nCurrent entry: {entry['name']}")
    print("\nEnter new values (leave blank to keep current):")
    
    updates = {}
    
    new_name = input(f"New name [{entry['name']}]: ").strip()
    if new_name:
        updates["name"] = new_name
    
    new_reason = input(f"New reason [{entry['reason'][:30]}...]: ").strip()
    if new_reason:
        updates["reason"] = new_reason
    
    new_threat = input(f"New threat level [{entry['threat_level']}]: ").strip()
    if new_threat:
        updates["threat_level"] = new_threat
    
    new_category = input(f"New category [{entry['category']}]: ").strip()
    if new_category:
        updates["category"] = new_category
    
    new_notes = input(f"New notes: ").strip()
    if new_notes:
        updates["notes"] = new_notes
    
    if not updates:
        print("❌ No updates provided!")
        return
    
    try:
        updated = manager.update_entry(identifier, **updates)
        if updated:
            print(f"\n✅ Entry updated successfully!")
            print(f"ID: {updated['id']}")
            print(f"Name: {updated['name']}")
            print(f"Last Updated: {updated['last_updated']}")
        else:
            print("❌ Failed to update entry!")
    except Exception as e:
        print(f"❌ Error updating entry: {e}")


def list_all_interactive(manager: BlacklistManager):
    """Interactive function to list all entries."""
    print("\n--- LIST ALL ENTRIES ---")
    print("Sort by: 1) Threat Level  2) Date Added  3) Name")
    sort_choice = input("Choose (default: 1): ").strip() or "1"
    
    sort_map = {"1": "threat_level", "2": "date_added", "3": "name"}
    sort_by = sort_map.get(sort_choice, "threat_level")
    
    try:
        entries = manager.list_all_entries(sort_by)
        if entries:
            print(f"\n✅ Total entries: {len(entries)}\n")
            for entry in entries:
                print(f"ID: {entry['id']} | {entry['name']}")
                print(f"  Threat: {entry['threat_level']} | Category: {entry['category']}")
                print(f"  Reason: {entry['reason'][:60]}...")
                print(f"  Added: {entry['date_added'][:10]}")
                print("-" * 60)
        else:
            print("❌ No entries in the blacklist.")
    except Exception as e:
        print(f"❌ Error listing entries: {e}")


def view_statistics(manager: BlacklistManager):
    """View blacklist statistics."""
    print("\n--- STATISTICS ---")
    try:
        stats = manager.get_statistics()
        
        print(f"\n📊 Total Entries: {stats['total_entries']}")
        print("\n🎯 Threat Level Breakdown:")
        for level, count in stats['threat_level_breakdown'].items():
            print(f"  {level}: {count}")
        
        print("\n📁 Category Breakdown:")
        for category, count in stats['category_breakdown'].items():
            print(f"  {category}: {count}")
        
        print(f"\n🕒 Last Updated: {stats['last_updated']}")
    except Exception as e:
        print(f"❌ Error getting statistics: {e}")


def export_blacklist(manager: BlacklistManager):
    """Export blacklist to a file."""
    print("\n--- EXPORT BLACKLIST ---")
    filename = input("Export filename (default: blacklist_export.json): ").strip()
    filename = filename or "blacklist_export.json"
    
    try:
        manager.export_to_file(filename)
        print(f"✅ Blacklist exported to {filename}")
    except Exception as e:
        print(f"❌ Export failed: {e}")


def import_blacklist(manager: BlacklistManager):
    """Import blacklist from a file."""
    print("\n--- IMPORT BLACKLIST ---")
    filename = input("Import filename: ").strip()
    
    if not filename or not os.path.exists(filename):
        print("❌ File not found!")
        return
    
    try:
        manager.import_from_file(filename)
        print(f"✅ Blacklist imported from {filename}")
    except Exception as e:
        print(f"❌ Import failed: {e}")


def main():
    """Main application loop."""
    print_banner()
    print("🚀 Initializing Blacklist Management System...")
    
    try:
        manager = BlacklistManager()
        print("✅ System initialized successfully!")
        print("\nℹ️  Running in Simple Mode (no AI features)")
        print("   For AI-powered features, set up API keys and use main.py\n")
    except Exception as e:
        print(f"❌ Failed to initialize: {e}")
        return
    
    # Main loop
    while True:
        print_menu()
        choice = input("\nSelect an option: ").strip()
        
        try:
            if choice == "1":
                add_entry_interactive(manager)
            elif choice == "2":
                remove_entry_interactive(manager)
            elif choice == "3":
                search_entries_interactive(manager)
            elif choice == "4":
                update_entry_interactive(manager)
            elif choice == "5":
                list_all_interactive(manager)
            elif choice == "6":
                view_statistics(manager)
            elif choice == "7":
                export_blacklist(manager)
            elif choice == "8":
                import_blacklist(manager)
            elif choice == "0":
                print("\n👋 Goodbye!")
                break
            else:
                print("❌ Invalid option. Please try again.")
        
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Please try again.")


if __name__ == "__main__":
    main()
