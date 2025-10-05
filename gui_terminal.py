"""
Terminal-Style GUI for Blacklist Management Tool
Mimics the CLI interface but in a graphical window
"""
import sys
import os
import pygame
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTextEdit, QLineEdit, QLabel, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal, QObject
from PyQt6.QtGui import QFont, QTextCursor, QColor, QPalette
from blacklist import BlacklistManager


class TerminalEmulator(QObject):
    """Handles the terminal-like interaction logic."""
    
    output_signal = pyqtSignal(str)
    prompt_signal = pyqtSignal(str)
    
    def __init__(self, manager):
        super().__init__()
        self.manager = manager
        self.state = "MENU"
        self.current_operation = None
        self.temp_data = {}
        
    def process_input(self, user_input):
        """Process user input based on current state."""
        if self.state == "MENU":
            self.handle_menu_choice(user_input)
        elif self.state == "ADD_NAME":
            self.handle_add_name(user_input)
        elif self.state == "ADD_REASON":
            self.handle_add_reason(user_input)
        elif self.state == "ADD_THREAT":
            self.handle_add_threat(user_input)
        elif self.state == "ADD_CATEGORY":
            self.handle_add_category(user_input)
        elif self.state == "ADD_NOTES":
            self.handle_add_notes(user_input)
        elif self.state == "REMOVE_ID":
            self.handle_remove(user_input)
        elif self.state == "SEARCH_QUERY":
            self.handle_search(user_input)
        elif self.state == "UPDATE_ID":
            self.handle_update_id(user_input)
        elif self.state == "UPDATE_FIELD":
            self.handle_update_field(user_input)
        elif self.state == "LIST_SORT":
            self.handle_list(user_input)
        elif self.state == "EXPORT_FILE":
            self.handle_export(user_input)
        elif self.state == "IMPORT_FILE":
            self.handle_import(user_input)
    
    def show_menu(self):
        """Display the main menu."""
        menu = """
           1. Add entry
           2. Remove entry
           3. Search
           4. Update
           5. List all
           0. Exit

"""
        self.output_signal.emit(menu)
        self.prompt_signal.emit("> ")
        self.state = "MENU"
    
    def handle_menu_choice(self, choice):
        """Handle menu selection."""
        choice = choice.strip()
        
        if choice == "1":
            self.start_add_entry()
        elif choice == "2":
            self.start_remove_entry()
        elif choice == "3":
            self.start_search()
        elif choice == "4":
            self.start_update()
        elif choice == "5":
            self.start_list()
        elif choice == "0":
            self.output_signal.emit("\n👋 Goodbye!\n")
            QApplication.quit()
        else:
            self.output_signal.emit("❌ Invalid option. Please try again.\n")
            self.show_menu()
    
    def start_add_entry(self):
        """Start the add entry process."""
        self.output_signal.emit("\n--- ADD NEW ENTRY ---\n")
        self.temp_data = {}
        self.state = "ADD_NAME"
        self.prompt_signal.emit("Name: ")
    
    def handle_add_name(self, name):
        """Handle name input for add entry."""
        name = name.strip()
        if not name:
            self.output_signal.emit("❌ Name is required!\n")
            self.show_menu()
            return
        
        self.temp_data['name'] = name
        self.state = "ADD_REASON"
        self.prompt_signal.emit("Reason for blacklisting: ")
    
    def handle_add_reason(self, reason):
        """Handle reason input for add entry."""
        reason = reason.strip()
        if not reason:
            self.output_signal.emit("❌ Reason is required!\n")
            self.show_menu()
            return
        
        self.temp_data['reason'] = reason
        self.output_signal.emit("\nThreat Levels: Low, Medium, High, Critical\n")
        self.state = "ADD_THREAT"
        self.prompt_signal.emit("Threat level (default: Medium): ")
    
    def handle_add_threat(self, threat):
        """Handle threat level input for add entry."""
        threat = threat.strip() or "Medium"
        self.temp_data['threat_level'] = threat
        self.state = "ADD_CATEGORY"
        self.prompt_signal.emit("Category (default: General): ")
    
    def handle_add_category(self, category):
        """Handle category input for add entry."""
        category = category.strip() or "General"
        self.temp_data['category'] = category
        self.state = "ADD_NOTES"
        self.prompt_signal.emit("Additional notes (optional): ")
    
    def handle_add_notes(self, notes):
        """Handle notes input and complete add entry."""
        self.temp_data['notes'] = notes.strip()
        
        try:
            entry = self.manager.add_entry(
                self.temp_data['name'],
                self.temp_data['reason'],
                self.temp_data['threat_level'],
                self.temp_data['notes'],
                self.temp_data['category']
            )
            
            result = f"""
✅ Entry added successfully!
ID: {entry['id']}
Name: {entry['name']}
Threat Level: {entry['threat_level']}
Date Added: {entry['date_added'][:19]}
"""
            self.output_signal.emit(result)
        except Exception as e:
            self.output_signal.emit(f"❌ Error adding entry: {e}\n")
        
        self.show_menu()
    
    def start_remove_entry(self):
        """Start the remove entry process."""
        self.output_signal.emit("\n--- REMOVE ENTRY ---\n")
        self.state = "REMOVE_ID"
        self.prompt_signal.emit("Enter entry ID or name: ")
    
    def handle_remove(self, identifier):
        """Handle remove entry."""
        identifier = identifier.strip()
        if not identifier:
            self.output_signal.emit("❌ Identifier is required!\n")
            self.show_menu()
            return
        
        try:
            removed = self.manager.remove_entry(identifier)
            if removed:
                self.output_signal.emit(f"\n✅ Entry removed successfully!\nRemoved: {removed['name']} (ID: {removed['id']})\n")
            else:
                self.output_signal.emit("❌ Entry not found!\n")
        except Exception as e:
            self.output_signal.emit(f"❌ Error removing entry: {e}\n")
        
        self.show_menu()
    
    def start_search(self):
        """Start the search process."""
        self.output_signal.emit("\n--- SEARCH ENTRIES ---\n")
        self.state = "SEARCH_QUERY"
        self.prompt_signal.emit("Search query (name, reason, notes): ")
    
    def handle_search(self, query):
        """Handle search."""
        query = query.strip()
        
        try:
            # Search with empty filters for threat_level and category
            results = self.manager.search_entries(query, "", "")
            if results:
                output = f"\n✅ Found {len(results)} entries:\n\n"
                for entry in results:
                    output += f"ID: {entry['id']} | {entry['name']}\n"
                    output += f"  Threat: {entry['threat_level']} | Category: {entry.get('category', 'General')}\n"
                    reason_text = entry['reason'][:60] if len(entry['reason']) > 60 else entry['reason']
                    output += f"  Reason: {reason_text}\n"
                    output += f"  Added: {entry['date_added'][:10]}\n"
                    output += "-" * 60 + "\n"
                self.output_signal.emit(output)
            else:
                self.output_signal.emit("❌ No entries found matching your criteria.\n")
        except Exception as e:
            self.output_signal.emit(f"❌ Error searching: {e}\n")
        
        self.show_menu()
    
    def start_update(self):
        """Start the update entry process."""
        self.output_signal.emit("\n--- UPDATE ENTRY ---\n")
        self.state = "UPDATE_ID"
        self.prompt_signal.emit("Enter entry ID or name: ")
    
    def handle_update_id(self, identifier):
        """Handle update entry ID."""
        identifier = identifier.strip()
        if not identifier:
            self.output_signal.emit("❌ Identifier is required!\n")
            self.show_menu()
            return
        
        entry = self.manager.get_entry(identifier)
        if not entry:
            self.output_signal.emit("❌ Entry not found!\n")
            self.show_menu()
            return
        
        self.temp_data = {'id': identifier, 'entry': entry, 'updates': {}}
        self.output_signal.emit(f"\nCurrent entry: {entry['name']}\n")
        self.output_signal.emit("\nEnter new values (leave blank to keep current):\n")
        self.output_signal.emit(f"Current name: {entry['name']}\n")
        self.state = "UPDATE_FIELD"
        self.current_field = "name"
        self.prompt_signal.emit("New name (or press Enter to skip): ")
    
    def handle_update_field(self, value):
        """Handle update field input."""
        value = value.strip()
        
        if self.current_field == "name":
            if value:
                self.temp_data['updates']['name'] = value
            self.output_signal.emit(f"Current reason: {self.temp_data['entry']['reason'][:30]}...\n")
            self.current_field = "reason"
            self.prompt_signal.emit("New reason (or press Enter to skip): ")
        
        elif self.current_field == "reason":
            if value:
                self.temp_data['updates']['reason'] = value
            self.output_signal.emit(f"Current threat level: {self.temp_data['entry']['threat_level']}\n")
            self.current_field = "threat"
            self.prompt_signal.emit("New threat level (or press Enter to skip): ")
        
        elif self.current_field == "threat":
            if value:
                self.temp_data['updates']['threat_level'] = value
            self.output_signal.emit(f"Current category: {self.temp_data['entry']['category']}\n")
            self.current_field = "category"
            self.prompt_signal.emit("New category (or press Enter to skip): ")
        
        elif self.current_field == "category":
            if value:
                self.temp_data['updates']['category'] = value
            self.current_field = "notes"
            self.prompt_signal.emit("New notes (or press Enter to skip): ")
        
        elif self.current_field == "notes":
            if value:
                self.temp_data['updates']['notes'] = value
            
            # Complete the update
            if not self.temp_data['updates']:
                self.output_signal.emit("❌ No updates provided!\n")
            else:
                try:
                    updated = self.manager.update_entry(self.temp_data['id'], **self.temp_data['updates'])
                    if updated:
                        self.output_signal.emit(f"\n✅ Entry updated successfully!\nID: {updated['id']}\nName: {updated['name']}\nLast Updated: {updated['last_updated'][:19]}\n")
                    else:
                        self.output_signal.emit("❌ Failed to update entry!\n")
                except Exception as e:
                    self.output_signal.emit(f"❌ Error updating entry: {e}\n")
            
            self.show_menu()
    
    def start_list(self):
        """Start the list entries process."""
        self.output_signal.emit("\n--- LIST ALL ENTRIES ---\n")
        self.output_signal.emit("Sort by: 1) Threat Level  2) Date Added  3) Name\n")
        self.state = "LIST_SORT"
        self.prompt_signal.emit("Choose (default: 1): ")
    
    def handle_list(self, choice):
        """Handle list entries."""
        choice = choice.strip() or "1"
        sort_map = {"1": "threat_level", "2": "date_added", "3": "name"}
        sort_by = sort_map.get(choice, "threat_level")
        
        try:
            entries = self.manager.list_all_entries(sort_by)
            if entries:
                output = f"\n✅ Total entries: {len(entries)}\n\n"
                for entry in entries:
                    output += f"ID: {entry['id']} | {entry['name']}\n"
                    output += f"  Threat: {entry['threat_level']} | Category: {entry.get('category', 'General')}\n"
                    reason_text = entry['reason'][:60] if len(entry['reason']) > 60 else entry['reason']
                    output += f"  Reason: {reason_text}\n"
                    output += f"  Added: {entry['date_added'][:10]}\n"
                    output += "-" * 40 + "\n"
                self.output_signal.emit(output)
            else:
                self.output_signal.emit("❌ No entries in the blacklist.\n")
        except Exception as e:
            self.output_signal.emit(f"❌ Error listing entries: {e}\n")
        
        self.show_menu()
    
    def show_statistics(self):
        """Show statistics."""
        self.output_signal.emit("\n--- STATISTICS ---\n")
        try:
            stats = self.manager.get_statistics()
            
            output = f"\nTotal: {stats['total_entries']}\n\n"
            output += "Threat Levels:\n"
            for level, count in stats['threat_level_breakdown'].items():
                output += f"  {level}: {count}\n"
            
            output += "\nCategories:\n"
            for category, count in stats['category_breakdown'].items():
                output += f"  {category}: {count}\n"
            
            output += f"\nUpdated: {stats['last_updated'][:19]}\n"
            
            self.output_signal.emit(output)
        except Exception as e:
            self.output_signal.emit(f"❌ Error: {e}\n")
        
        self.show_menu()
    
    def start_export(self):
        """Start export process."""
        self.output_signal.emit("\n--- EXPORT BLACKLIST ---\n")
        self.state = "EXPORT_FILE"
        self.prompt_signal.emit("Export filename (default: blacklist_export.json): ")
    
    def handle_export(self, filename):
        """Handle export."""
        filename = filename.strip() or "blacklist_export.json"
        
        try:
            self.manager.export_to_file(filename)
            self.output_signal.emit(f"✅ Blacklist exported to {filename}\n")
        except Exception as e:
            self.output_signal.emit(f"❌ Export failed: {e}\n")
        
        self.show_menu()
    
    def start_import(self):
        """Start import process."""
        self.output_signal.emit("\n--- IMPORT BLACKLIST ---\n")
        self.state = "IMPORT_FILE"
        self.prompt_signal.emit("Import filename: ")
    
    def handle_import(self, filename):
        """Handle import."""
        filename = filename.strip()
        
        if not filename or not os.path.exists(filename):
            self.output_signal.emit("❌ File not found!\n")
            self.show_menu()
            return
        
        try:
            self.manager.import_from_file(filename)
            self.output_signal.emit(f"✅ Blacklist imported from {filename}\n")
        except Exception as e:
            self.output_signal.emit(f"❌ Import failed: {e}\n")
        
        self.show_menu()


class TerminalGUI(QMainWindow):
    """Terminal-style GUI window."""
    
    def __init__(self):
        super().__init__()
        self.manager = BlacklistManager()
        self.terminal = TerminalEmulator(self.manager)
        
        # Initialize pygame mixer for MIDI playback
        # Set ENABLE_MUSIC to False to disable background music
        self.ENABLE_MUSIC = True  # Dramatic theme enabled
        
        if self.ENABLE_MUSIC:
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            self.start_background_music()
        
        self.setup_ui()
        self.connect_signals()
        self.show_banner()
        
        # Enable dragging
        self.dragging = False
        self.offset = None
    
    def start_background_music(self):
        """Start playing the haunting theme in the background."""
        try:
            # Try WAV first (more compatible), then MIDI
            audio_file = "blacklist_theme.wav"
            if not os.path.exists(audio_file):
                audio_file = "blacklist_theme.mid"
            
            if os.path.exists(audio_file):
                pygame.mixer.music.load(audio_file)
                pygame.mixer.music.set_volume(0.3)  # 30% volume for background
                pygame.mixer.music.play(-1)  # Loop indefinitely
                print(f"♪ Playing: {audio_file}")
        except Exception as e:
            print(f"Could not load music: {e}")
    
    def setup_ui(self):
        """Set up the user interface."""
        # Remove default title bar and frame
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        
        # Pocket-sized window
        self.setFixedSize(500, 400)
        
        # Set window style to match terminal theme
        self.setStyleSheet("""
            QMainWindow {
                background-color: #141414;
                border: 2px solid #ff0000;
            }
            QWidget {
                background-color: #141414;
            }
        """)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Custom title bar
        title_bar = QFrame()
        title_bar.setStyleSheet("""
            QFrame {
                background-color: #ff0000;
                border-bottom: 1px solid #ff0000;
            }
        """)
        title_bar.setFixedHeight(30)
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(10, 0, 10, 0)
        
        title_label = QLabel("⬛ BLACKLIST v1.0")
        title_label.setFont(QFont("Courier", 10, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #000000;")
        
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(25, 25)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #000000;
                color: #ff0000;
                border: 1px solid #000000;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #ff0000;
                color: #000000;
            }
        """)
        close_btn.clicked.connect(self.close)
        
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        title_layout.addWidget(close_btn)
        
        layout.addWidget(title_bar)
        
        # Output display (terminal screen)
        self.output_display = QTextEdit()
        self.output_display.setReadOnly(True)
        # Font size 11, RED color
        self.output_display.setFont(QFont("Courier", 11))
        
        # Set terminal colors (dark theme with RED text)
        palette = self.output_display.palette()
        palette.setColor(QPalette.ColorRole.Base, QColor(20, 20, 20))
        palette.setColor(QPalette.ColorRole.Text, QColor(255, 0, 0))  # RED
        self.output_display.setPalette(palette)
        
        layout.addWidget(self.output_display)
        
        # Input area
        input_frame = QFrame()
        input_frame.setStyleSheet("""
            QFrame {
                background-color: #0a0a0a;
                border-top: 2px solid #ff0000;
                padding: 5px;
            }
        """)
        input_layout = QHBoxLayout(input_frame)
        
        self.prompt_label = QLabel(">")
        # Font size 11, RED color
        self.prompt_label.setFont(QFont("Courier", 11, QFont.Weight.Bold))
        self.prompt_label.setStyleSheet("color: #ff0000;")
        
        self.input_field = QLineEdit()
        # Font size 11, RED color
        self.input_field.setFont(QFont("Courier", 11))
        self.input_field.setStyleSheet("""
            QLineEdit {
                background-color: #2a2a2a;
                color: #ff0000;
                border: 1px solid #ff0000;
                padding: 5px;
            }
        """)
        self.input_field.returnPressed.connect(self.handle_input)
        
        input_layout.addWidget(self.prompt_label)
        input_layout.addWidget(self.input_field)
        
        # Music toggle button
        if self.ENABLE_MUSIC:
            self.music_enabled = True
            music_label = QLabel("Music:")
            music_label.setFont(QFont("Courier", 8))
            music_label.setStyleSheet("color: #ff0000; margin-left: 10px;")
            
            self.music_toggle_btn = QPushButton("")  # Empty when music is playing
            self.music_toggle_btn.setFixedSize(12, 12)
            self.music_toggle_btn.setFont(QFont("Courier", 7, QFont.Weight.Bold))
            self.music_toggle_btn.setStyleSheet("""
                QPushButton {
                    background-color: #000000;
                    color: #ff0000;
                    border: 1px solid #ff0000;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #ff0000;
                    color: #000000;
                    border: 1px solid #ff0000;
                }
            """)
            self.music_toggle_btn.clicked.connect(self.toggle_music)
            
            input_layout.addWidget(music_label)
            input_layout.addWidget(self.music_toggle_btn)
        
        layout.addWidget(input_frame)
        
        # Focus on input
        self.input_field.setFocus()
    
    def connect_signals(self):
        """Connect terminal emulator signals."""
        self.terminal.output_signal.connect(self.append_output)
        self.terminal.prompt_signal.connect(self.set_prompt)
    
    def show_banner(self):
        """Show the application banner."""
        banner = """
 ██████╗ ██╗      █████╗  ██████╗██╗  ██╗
 ██╔══██╗██║     ██╔══██╗██╔════╝██║ ██╔╝
 ██████╔╝██║     ███████║██║     █████╔╝ 
 ██╔══██╗██║     ██╔══██║██║     ██╔═██╗ 
 ██████╔╝███████╗██║  ██║╚██████╗██║  ██╗
 ╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝
 ██╗     ██╗███████╗████████╗            
 ██║     ██║██╔════╝╚══██╔══╝            
 ██║     ██║███████╗   ██║               
 ██║     ██║╚════██║   ██║               
 ███████╗██║███████║   ██║               
 ╚══════╝╚═╝╚══════╝   ╚═╝               
                                         
Respect

"""
        self.append_output(banner)
        self.terminal.show_menu()
    
    def append_output(self, text):
        """Append text to the output display."""
        self.output_display.moveCursor(QTextCursor.MoveOperation.End)
        self.output_display.insertPlainText(text)
        self.output_display.moveCursor(QTextCursor.MoveOperation.End)
    
    def set_prompt(self, prompt_text):
        """Set the prompt label."""
        self.prompt_label.setText(prompt_text)
    
    def handle_input(self):
        """Handle user input."""
        user_input = self.input_field.text()
        
        # Echo input to display
        self.append_output(f"{self.prompt_label.text()}{user_input}\n")
        
        # Clear input field
        self.input_field.clear()
        
        # Process input
        self.terminal.process_input(user_input)
    
    def mousePressEvent(self, event):
        """Handle mouse press for window dragging."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.offset = event.pos()
    
    def mouseMoveEvent(self, event):
        """Handle mouse move for window dragging."""
        if self.dragging and self.offset is not None:
            self.move(self.mapToGlobal(event.pos() - self.offset))
    
    def mouseReleaseEvent(self, event):
        """Handle mouse release."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False
    
    def toggle_music(self):
        """Toggle music on/off."""
        if self.music_enabled:
            # Turn off music - show X
            pygame.mixer.music.pause()
            self.music_enabled = False
            self.music_toggle_btn.setText("X")
            self.music_toggle_btn.setStyleSheet("""
                QPushButton {
                    background-color: #000000;
                    color: #ff0000;
                    border: 1px solid #ff0000;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #ff0000;
                    color: #000000;
                    border: 1px solid #ff0000;
                }
            """)
        else:
            # Turn on music - empty box
            pygame.mixer.music.unpause()
            self.music_enabled = True
            self.music_toggle_btn.setText("")
            self.music_toggle_btn.setStyleSheet("""
                QPushButton {
                    background-color: #000000;
                    color: #ff0000;
                    border: 1px solid #ff0000;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #ff0000;
                    color: #000000;
                    border: 1px solid #ff0000;
                }
            """)
    
    def closeEvent(self, event):
        """Handle window close event - stop music."""
        if self.ENABLE_MUSIC:
            pygame.mixer.music.stop()
            pygame.mixer.quit()
        event.accept()


def main():
    """Main entry point for the terminal GUI application."""
    app = QApplication(sys.argv)
    
    window = TerminalGUI()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
