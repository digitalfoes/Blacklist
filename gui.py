"""
Modern GUI for Blacklist Management Tool
Built with PyQt6 - No API Key Required
"""
import sys
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QTextEdit, QTableWidget, QTableWidgetItem,
    QComboBox, QMessageBox, QDialog, QDialogButtonBox, QFormLayout,
    QTabWidget, QGroupBox, QSplitter, QHeaderView
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QColor, QIcon
from blacklist import BlacklistManager


class AddEntryDialog(QDialog):
    """Dialog for adding a new blacklist entry."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Entry")
        self.setMinimumWidth(500)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QFormLayout()
        
        # Input fields
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter name...")
        
        self.reason_input = QTextEdit()
        self.reason_input.setPlaceholderText("Enter reason for blacklisting...")
        self.reason_input.setMaximumHeight(100)
        
        self.threat_combo = QComboBox()
        self.threat_combo.addItems(["Low", "Medium", "High", "Critical"])
        self.threat_combo.setCurrentText("Medium")
        
        self.category_input = QLineEdit()
        self.category_input.setText("General")
        self.category_input.setPlaceholderText("Enter category...")
        
        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Additional notes (optional)...")
        self.notes_input.setMaximumHeight(80)
        
        # Add to layout
        layout.addRow("Name:*", self.name_input)
        layout.addRow("Reason:*", self.reason_input)
        layout.addRow("Threat Level:", self.threat_combo)
        layout.addRow("Category:", self.category_input)
        layout.addRow("Notes:", self.notes_input)
        
        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)
        
        self.setLayout(layout)
    
    def get_data(self):
        """Get the entered data."""
        return {
            "name": self.name_input.text().strip(),
            "reason": self.reason_input.toPlainText().strip(),
            "threat_level": self.threat_combo.currentText(),
            "category": self.category_input.text().strip() or "General",
            "notes": self.notes_input.toPlainText().strip()
        }


class EditEntryDialog(QDialog):
    """Dialog for editing an existing entry."""
    
    def __init__(self, entry, parent=None):
        super().__init__(parent)
        self.entry = entry
        self.setWindowTitle(f"Edit Entry: {entry['name']}")
        self.setMinimumWidth(500)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QFormLayout()
        
        # Input fields pre-filled with current values
        self.name_input = QLineEdit(self.entry['name'])
        
        self.reason_input = QTextEdit()
        self.reason_input.setPlainText(self.entry['reason'])
        self.reason_input.setMaximumHeight(100)
        
        self.threat_combo = QComboBox()
        self.threat_combo.addItems(["Low", "Medium", "High", "Critical"])
        self.threat_combo.setCurrentText(self.entry['threat_level'])
        
        self.category_input = QLineEdit(self.entry.get('category', 'General'))
        
        self.notes_input = QTextEdit()
        self.notes_input.setPlainText(self.entry.get('notes', ''))
        self.notes_input.setMaximumHeight(80)
        
        # Add to layout
        layout.addRow("Name:", self.name_input)
        layout.addRow("Reason:", self.reason_input)
        layout.addRow("Threat Level:", self.threat_combo)
        layout.addRow("Category:", self.category_input)
        layout.addRow("Notes:", self.notes_input)
        
        # Info labels
        info_label = QLabel(f"ID: {self.entry['id']} | Added: {self.entry['date_added'][:10]}")
        info_label.setStyleSheet("color: gray; font-size: 10px;")
        layout.addRow(info_label)
        
        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)
        
        self.setLayout(layout)
    
    def get_updates(self):
        """Get the updated data."""
        return {
            "name": self.name_input.text().strip(),
            "reason": self.reason_input.toPlainText().strip(),
            "threat_level": self.threat_combo.currentText(),
            "category": self.category_input.text().strip(),
            "notes": self.notes_input.toPlainText().strip()
        }


class BlacklistGUI(QMainWindow):
    """Main GUI window for Blacklist Management."""
    
    def __init__(self):
        super().__init__()
        self.manager = BlacklistManager()
        self.current_entries = []
        self.setup_ui()
        self.load_entries()
    
    def setup_ui(self):
        """Set up the user interface."""
        self.setWindowTitle("Blacklist Management Tool")
        self.setMinimumSize(1000, 700)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Header
        header = self.create_header()
        main_layout.addWidget(header)
        
        # Tabs
        tabs = QTabWidget()
        tabs.addTab(self.create_entries_tab(), "📋 Entries")
        tabs.addTab(self.create_statistics_tab(), "📊 Statistics")
        tabs.addTab(self.create_search_tab(), "🔍 Search")
        main_layout.addWidget(tabs)
        
        # Status bar
        self.statusBar().showMessage("Ready")
    
    def create_header(self):
        """Create the header section."""
        header = QGroupBox()
        layout = QHBoxLayout()
        
        # Title
        title = QLabel("🛡️ Blacklist Management Tool")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        layout.addStretch()
        
        # Action buttons
        add_btn = QPushButton("➕ Add Entry")
        add_btn.clicked.connect(self.add_entry)
        add_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 8px 16px; font-weight: bold;")
        
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.clicked.connect(self.load_entries)
        refresh_btn.setStyleSheet("padding: 8px 16px;")
        
        layout.addWidget(add_btn)
        layout.addWidget(refresh_btn)
        
        header.setLayout(layout)
        return header
    
    def create_entries_tab(self):
        """Create the entries management tab."""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Filter controls
        filter_box = QGroupBox("Filters")
        filter_layout = QHBoxLayout()
        
        filter_layout.addWidget(QLabel("Threat Level:"))
        self.threat_filter = QComboBox()
        self.threat_filter.addItems(["All", "Low", "Medium", "High", "Critical"])
        self.threat_filter.currentTextChanged.connect(self.apply_filters)
        filter_layout.addWidget(self.threat_filter)
        
        filter_layout.addWidget(QLabel("Sort By:"))
        self.sort_combo = QComboBox()
        self.sort_combo.addItems(["Threat Level", "Date Added", "Name"])
        self.sort_combo.currentTextChanged.connect(self.apply_filters)
        filter_layout.addWidget(self.sort_combo)
        
        filter_layout.addStretch()
        filter_box.setLayout(filter_layout)
        layout.addWidget(filter_box)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Threat", "Category", "Date Added", "Actions"])
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setAlternatingRowColors(True)
        layout.addWidget(self.table)
        
        widget.setLayout(layout)
        return widget
    
    def create_statistics_tab(self):
        """Create the statistics tab."""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Statistics display
        self.stats_text = QTextEdit()
        self.stats_text.setReadOnly(True)
        self.stats_text.setFont(QFont("Courier", 10))
        layout.addWidget(self.stats_text)
        
        # Refresh button
        refresh_btn = QPushButton("🔄 Refresh Statistics")
        refresh_btn.clicked.connect(self.update_statistics)
        layout.addWidget(refresh_btn)
        
        widget.setLayout(layout)
        return widget
    
    def create_search_tab(self):
        """Create the search tab."""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Search controls
        search_box = QGroupBox("Search Criteria")
        search_layout = QFormLayout()
        
        self.search_query = QLineEdit()
        self.search_query.setPlaceholderText("Search in name, reason, notes...")
        
        self.search_threat = QComboBox()
        self.search_threat.addItems(["Any", "Low", "Medium", "High", "Critical"])
        
        self.search_category = QLineEdit()
        self.search_category.setPlaceholderText("Leave empty for all categories")
        
        search_layout.addRow("Query:", self.search_query)
        search_layout.addRow("Threat Level:", self.search_threat)
        search_layout.addRow("Category:", self.search_category)
        
        search_btn = QPushButton("🔍 Search")
        search_btn.clicked.connect(self.perform_search)
        search_btn.setStyleSheet("background-color: #2196F3; color: white; padding: 8px; font-weight: bold;")
        search_layout.addRow(search_btn)
        
        search_box.setLayout(search_layout)
        layout.addWidget(search_box)
        
        # Results
        self.search_results = QTextEdit()
        self.search_results.setReadOnly(True)
        layout.addWidget(QLabel("Search Results:"))
        layout.addWidget(self.search_results)
        
        widget.setLayout(layout)
        return widget
    
    def load_entries(self):
        """Load all entries into the table."""
        try:
            self.current_entries = self.manager.list_all_entries()
            self.apply_filters()
            self.update_statistics()
            self.statusBar().showMessage(f"Loaded {len(self.current_entries)} entries")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load entries: {e}")
    
    def apply_filters(self):
        """Apply filters and update the table."""
        # Get filter values
        threat_filter = self.threat_filter.currentText()
        sort_by_text = self.sort_combo.currentText()
        
        # Map sort option
        sort_map = {
            "Threat Level": "threat_level",
            "Date Added": "date_added",
            "Name": "name"
        }
        sort_by = sort_map.get(sort_by_text, "threat_level")
        
        # Filter entries
        filtered = self.current_entries
        if threat_filter != "All":
            filtered = [e for e in filtered if e['threat_level'] == threat_filter]
        
        # Sort
        if sort_by == "threat_level":
            threat_order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
            filtered.sort(key=lambda x: threat_order.get(x.get("threat_level", "Medium"), 2))
        elif sort_by == "date_added":
            filtered.sort(key=lambda x: x.get("date_added", ""), reverse=True)
        else:
            filtered.sort(key=lambda x: x.get("name", "").lower())
        
        # Update table
        self.populate_table(filtered)
    
    def populate_table(self, entries):
        """Populate the table with entries."""
        self.table.setRowCount(len(entries))
        
        for row, entry in enumerate(entries):
            # ID
            self.table.setItem(row, 0, QTableWidgetItem(entry['id']))
            
            # Name
            self.table.setItem(row, 1, QTableWidgetItem(entry['name']))
            
            # Threat Level with color
            threat_item = QTableWidgetItem(entry['threat_level'])
            threat_colors = {
                "Critical": QColor(255, 0, 0, 50),
                "High": QColor(255, 165, 0, 50),
                "Medium": QColor(255, 255, 0, 50),
                "Low": QColor(0, 255, 0, 50)
            }
            threat_item.setBackground(threat_colors.get(entry['threat_level'], QColor(200, 200, 200)))
            self.table.setItem(row, 2, threat_item)
            
            # Category
            self.table.setItem(row, 3, QTableWidgetItem(entry.get('category', 'General')))
            
            # Date
            date_str = entry['date_added'][:10] if 'date_added' in entry else "N/A"
            self.table.setItem(row, 4, QTableWidgetItem(date_str))
            
            # Actions
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(4, 2, 4, 2)
            
            view_btn = QPushButton("👁️")
            view_btn.setToolTip("View Details")
            view_btn.clicked.connect(lambda checked, e=entry: self.view_entry(e))
            
            edit_btn = QPushButton("✏️")
            edit_btn.setToolTip("Edit Entry")
            edit_btn.clicked.connect(lambda checked, e=entry: self.edit_entry(e))
            
            delete_btn = QPushButton("🗑️")
            delete_btn.setToolTip("Delete Entry")
            delete_btn.setStyleSheet("color: red;")
            delete_btn.clicked.connect(lambda checked, e=entry: self.delete_entry(e))
            
            actions_layout.addWidget(view_btn)
            actions_layout.addWidget(edit_btn)
            actions_layout.addWidget(delete_btn)
            
            self.table.setCellWidget(row, 5, actions_widget)
    
    def add_entry(self):
        """Add a new entry."""
        dialog = AddEntryDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            
            if not data['name'] or not data['reason']:
                QMessageBox.warning(self, "Validation Error", "Name and Reason are required!")
                return
            
            try:
                entry = self.manager.add_entry(
                    data['name'],
                    data['reason'],
                    data['threat_level'],
                    data['notes'],
                    data['category']
                )
                QMessageBox.information(self, "Success", f"Entry '{entry['name']}' added successfully!")
                self.load_entries()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to add entry: {e}")
    
    def view_entry(self, entry):
        """View entry details."""
        details = f"""
<h2>{entry['name']}</h2>
<p><b>ID:</b> {entry['id']}</p>
<p><b>Threat Level:</b> <span style='color: red;'>{entry['threat_level']}</span></p>
<p><b>Category:</b> {entry.get('category', 'General')}</p>
<p><b>Date Added:</b> {entry['date_added'][:19]}</p>
<p><b>Last Updated:</b> {entry.get('last_updated', 'N/A')[:19]}</p>
<hr>
<p><b>Reason:</b></p>
<p>{entry['reason']}</p>
<p><b>Notes:</b></p>
<p>{entry.get('notes', 'No notes')}</p>
        """
        
        msg = QMessageBox(self)
        msg.setWindowTitle("Entry Details")
        msg.setTextFormat(Qt.TextFormat.RichText)
        msg.setText(details)
        msg.exec()
    
    def edit_entry(self, entry):
        """Edit an existing entry."""
        dialog = EditEntryDialog(entry, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            updates = dialog.get_updates()
            
            try:
                self.manager.update_entry(entry['id'], **updates)
                QMessageBox.information(self, "Success", "Entry updated successfully!")
                self.load_entries()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to update entry: {e}")
    
    def delete_entry(self, entry):
        """Delete an entry."""
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete '{entry['name']}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.manager.remove_entry(entry['id'])
                QMessageBox.information(self, "Success", "Entry deleted successfully!")
                self.load_entries()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete entry: {e}")
    
    def update_statistics(self):
        """Update the statistics display."""
        try:
            stats = self.manager.get_statistics()
            
            stats_html = f"""
<h2>📊 Blacklist Statistics</h2>
<p><b>Total Entries:</b> {stats['total_entries']}</p>

<h3>🎯 Threat Level Breakdown:</h3>
<ul>
"""
            for level, count in stats['threat_level_breakdown'].items():
                stats_html += f"<li><b>{level}:</b> {count}</li>"
            
            stats_html += """
</ul>

<h3>📁 Category Breakdown:</h3>
<ul>
"""
            for category, count in stats['category_breakdown'].items():
                stats_html += f"<li><b>{category}:</b> {count}</li>"
            
            stats_html += f"""
</ul>

<p><b>Last Updated:</b> {stats['last_updated'][:19]}</p>
            """
            
            self.stats_text.setHtml(stats_html)
        except Exception as e:
            self.stats_text.setPlainText(f"Error loading statistics: {e}")
    
    def perform_search(self):
        """Perform a search."""
        query = self.search_query.text().strip()
        threat = self.search_threat.currentText()
        category = self.search_category.text().strip()
        
        threat_level = "" if threat == "Any" else threat
        
        try:
            results = self.manager.search_entries(query, threat_level, category)
            
            if results:
                results_html = f"<h3>Found {len(results)} entries:</h3><hr>"
                for entry in results:
                    results_html += f"""
<div style='margin-bottom: 15px; padding: 10px; background-color: #f0f0f0;'>
    <h4>{entry['name']} <span style='color: red;'>({entry['threat_level']})</span></h4>
    <p><b>ID:</b> {entry['id']} | <b>Category:</b> {entry.get('category', 'General')}</p>
    <p><b>Reason:</b> {entry['reason'][:100]}...</p>
    <p><b>Added:</b> {entry['date_added'][:10]}</p>
</div>
                    """
                self.search_results.setHtml(results_html)
            else:
                self.search_results.setPlainText("No entries found matching your criteria.")
        except Exception as e:
            self.search_results.setPlainText(f"Search error: {e}")


def main():
    """Main entry point for the GUI application."""
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    window = BlacklistGUI()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
