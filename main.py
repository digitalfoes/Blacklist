"""
Main entry point for the Blacklist Management Tool with CrewAI
"""
import os
from dotenv import load_dotenv
from crew import BlacklistCrew
from blacklist import BlacklistManager


def print_banner():
    """Print the application banner."""
    print("\n" + "="*60)
    print("  BLACKLIST MANAGEMENT TOOL - Powered by CrewAI")
    print("="*60 + "\n")


def print_menu():
    """Print the main menu."""
    print("\n--- MAIN MENU ---")
    print("\n📋 Blacklist Operations:")
    print("1. Add new blacklist entry")
    print("2. Remove entry")
    print("3. Search entries")
    print("4. Update entry")
    print("5. List all entries")
    print("6. Generate report")
    print("7. Analyze threat (without adding)")
    print("8. View statistics")
    print("9. Export blacklist")
    print("10. Import blacklist")
    print("\n🐍 Python Pro - Code Quality:")
    print("11. Review code")
    print("12. Optimize code")
    print("13. Refactor code")
    print("14. Create testing strategy")
    print("15. Modernize code")
    print("\n0. Exit")
    print("-" * 40)


def add_entry_interactive(crew: BlacklistCrew):
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
    
    entry_data = {
        "name": name,
        "reason": reason,
        "threat_level": threat_level,
        "category": category,
        "notes": notes
    }
    
    print("\n🤖 AI agents are analyzing and adding the entry...")
    result = crew.add_entry(entry_data)
    print(f"\n✅ Result:\n{result}")


def remove_entry_interactive(crew: BlacklistCrew):
    """Interactive function to remove an entry."""
    print("\n--- REMOVE ENTRY ---")
    identifier = input("Enter entry ID or name: ").strip()
    if not identifier:
        print("❌ Identifier is required!")
        return
    
    print("\n🤖 AI agents are processing the removal...")
    result = crew.remove_entry(identifier)
    print(f"\n✅ Result:\n{result}")


def search_entries_interactive(crew: BlacklistCrew):
    """Interactive function to search entries."""
    print("\n--- SEARCH ENTRIES ---")
    query = input("Search query (name, reason, notes): ").strip()
    
    print("\n🤖 AI agents are searching...")
    result = crew.search_entries(query)
    print(f"\n✅ Results:\n{result}")


def update_entry_interactive(crew: BlacklistCrew):
    """Interactive function to update an entry."""
    print("\n--- UPDATE ENTRY ---")
    identifier = input("Enter entry ID or name: ").strip()
    if not identifier:
        print("❌ Identifier is required!")
        return
    
    print("\nEnter new values (leave blank to keep current):")
    updates = {}
    
    new_name = input("New name: ").strip()
    if new_name:
        updates["name"] = new_name
    
    new_reason = input("New reason: ").strip()
    if new_reason:
        updates["reason"] = new_reason
    
    new_threat = input("New threat level: ").strip()
    if new_threat:
        updates["threat_level"] = new_threat
    
    new_category = input("New category: ").strip()
    if new_category:
        updates["category"] = new_category
    
    new_notes = input("New notes: ").strip()
    if new_notes:
        updates["notes"] = new_notes
    
    if not updates:
        print("❌ No updates provided!")
        return
    
    print("\n🤖 AI agents are updating the entry...")
    result = crew.update_entry(identifier, updates)
    print(f"\n✅ Result:\n{result}")


def list_all_interactive(crew: BlacklistCrew):
    """Interactive function to list all entries."""
    print("\n--- LIST ALL ENTRIES ---")
    print("Filter by threat level (optional):")
    print("Options: Low, Medium, High, Critical")
    filter_criteria = input("Filter (leave blank for all): ").strip() or None
    
    print("\n🤖 AI agents are retrieving entries...")
    result = crew.list_all_entries(filter_criteria)
    print(f"\n✅ Entries:\n{result}")


def generate_report_interactive(crew: BlacklistCrew):
    """Interactive function to generate a report."""
    print("\n--- GENERATE REPORT ---")
    print("Report types: summary, detailed, statistics, trends")
    report_type = input("Report type (default: summary): ").strip() or "summary"
    
    print("\n🤖 AI agents are generating the report...")
    result = crew.generate_report(report_type)
    print(f"\n✅ Report:\n{result}")


def analyze_threat_interactive(crew: BlacklistCrew):
    """Interactive function to analyze a threat without adding it."""
    print("\n--- ANALYZE THREAT ---")
    name = input("Name/Entity: ").strip()
    reason = input("Reason/Context: ").strip()
    context = input("Additional context: ").strip()
    
    entry_data = {
        "name": name,
        "reason": reason,
        "context": context
    }
    
    print("\n🤖 AI agents are analyzing the threat...")
    result = crew.analyze_threat(entry_data)
    print(f"\n✅ Analysis:\n{result}")


def view_statistics(manager: BlacklistManager):
    """View blacklist statistics."""
    print("\n--- STATISTICS ---")
    stats = manager.get_statistics()
    
    print(f"\n📊 Total Entries: {stats['total_entries']}")
    print("\n🎯 Threat Level Breakdown:")
    for level, count in stats['threat_level_breakdown'].items():
        print(f"  {level}: {count}")
    
    print("\n📁 Category Breakdown:")
    for category, count in stats['category_breakdown'].items():
        print(f"  {category}: {count}")
    
    print(f"\n🕒 Last Updated: {stats['last_updated']}")


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


def review_code_interactive(crew: BlacklistCrew):
    """Interactive function to review code with Python Pro agent."""
    print("\n--- PYTHON PRO: CODE REVIEW ---")
    file_path = input("File path to review: ").strip()
    
    if not file_path or not os.path.exists(file_path):
        print("❌ File not found!")
        return
    
    print("\nFocus areas (optional, comma-separated):")
    print("Examples: performance, security, type hints, error handling")
    focus_input = input("Focus areas (leave blank for general review): ").strip()
    focus_areas = [area.strip() for area in focus_input.split(",")] if focus_input else None
    
    print("\n🤖 Python Pro agent is reviewing your code...")
    result = crew.review_code(file_path, focus_areas)
    print(f"\n✅ Code Review:\n{result}")


def optimize_code_interactive(crew: BlacklistCrew):
    """Interactive function to optimize code with Python Pro agent."""
    print("\n--- PYTHON PRO: CODE OPTIMIZATION ---")
    file_path = input("File path to optimize: ").strip()
    
    if not file_path or not os.path.exists(file_path):
        print("❌ File not found!")
        return
    
    print("\nOptimization types: performance, memory, readability")
    opt_type = input("Optimization type (default: performance): ").strip() or "performance"
    
    print("\n🤖 Python Pro agent is optimizing your code...")
    result = crew.optimize_code(file_path, opt_type)
    print(f"\n✅ Optimization Results:\n{result}")


def refactor_code_interactive(crew: BlacklistCrew):
    """Interactive function to refactor code with Python Pro agent."""
    print("\n--- PYTHON PRO: CODE REFACTORING ---")
    file_path = input("File path to refactor: ").strip()
    
    if not file_path or not os.path.exists(file_path):
        print("❌ File not found!")
        return
    
    print("\nRefactoring goals (comma-separated):")
    print("Examples: apply SOLID principles, add type hints, improve error handling")
    goals_input = input("Goals: ").strip()
    
    if not goals_input:
        print("❌ At least one refactoring goal is required!")
        return
    
    goals = [goal.strip() for goal in goals_input.split(",")]
    
    print("\n🤖 Python Pro agent is refactoring your code...")
    result = crew.refactor_code(file_path, goals)
    print(f"\n✅ Refactoring Results:\n{result}")


def create_tests_interactive(crew: BlacklistCrew):
    """Interactive function to create testing strategy with Python Pro agent."""
    print("\n--- PYTHON PRO: TESTING STRATEGY ---")
    file_path = input("File path to create tests for: ").strip()
    
    if not file_path or not os.path.exists(file_path):
        print("❌ File not found!")
        return
    
    print("\n🤖 Python Pro agent is designing a testing strategy...")
    result = crew.create_testing_strategy(file_path)
    print(f"\n✅ Testing Strategy:\n{result}")


def modernize_code_interactive(crew: BlacklistCrew):
    """Interactive function to modernize code with Python Pro agent."""
    print("\n--- PYTHON PRO: CODE MODERNIZATION ---")
    file_path = input("File path to modernize: ").strip()
    
    if not file_path or not os.path.exists(file_path):
        print("❌ File not found!")
        return
    
    print("\n🤖 Python Pro agent is modernizing your code to Python 3.12+...")
    result = crew.modernize_code(file_path)
    print(f"\n✅ Modernization Results:\n{result}")


def main():
    """Main application loop."""
    # Load environment variables
    load_dotenv()
    
    # Check for API key
    if not os.getenv("OPENAI_API_KEY") and not os.getenv("ANTHROPIC_API_KEY"):
        print("\n⚠️  WARNING: No API key found in environment variables!")
        print("Please create a .env file with your API key.")
        print("Example: OPENAI_API_KEY=your_key_here\n")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            return
    
    # Initialize managers
    print("🚀 Initializing Blacklist Management System...")
    manager = BlacklistManager()
    crew = BlacklistCrew()
    
    print_banner()
    print("✅ System initialized successfully!")
    
    # Main loop
    while True:
        print_menu()
        choice = input("\nSelect an option: ").strip()
        
        try:
            if choice == "1":
                add_entry_interactive(crew)
            elif choice == "2":
                remove_entry_interactive(crew)
            elif choice == "3":
                search_entries_interactive(crew)
            elif choice == "4":
                update_entry_interactive(crew)
            elif choice == "5":
                list_all_interactive(crew)
            elif choice == "6":
                generate_report_interactive(crew)
            elif choice == "7":
                analyze_threat_interactive(crew)
            elif choice == "8":
                view_statistics(manager)
            elif choice == "9":
                export_blacklist(manager)
            elif choice == "10":
                import_blacklist(manager)
            elif choice == "11":
                review_code_interactive(crew)
            elif choice == "12":
                optimize_code_interactive(crew)
            elif choice == "13":
                refactor_code_interactive(crew)
            elif choice == "14":
                create_tests_interactive(crew)
            elif choice == "15":
                modernize_code_interactive(crew)
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
            print("Please try again or contact support.")


if __name__ == "__main__":
    main()
