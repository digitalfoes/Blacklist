# Blacklist Management Tool with CrewAI

A blacklist management system powered by CrewAI agents that help users manage their personal blacklist of enemies, with integrated Python code quality tools.

## Features

- **AI-Powered Management**: Uses CrewAI agents to intelligently manage blacklist entries
- **Multi-Agent System**: Specialized agents for different aspects of blacklist management
- **Flexible Operations**: Add, remove, search, and analyze blacklist entries
- **Python Pro Agent**: Code review, optimization, refactoring, and modernization using Python 3.12+ best practices

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment:
```bash
cp .env.example .env
# Edit .env and add your API keys
```

3. Run the tool:
```bash
python main.py
```

## Project Structure

- `main.py` - Main entry point
- `agents.py` - CrewAI agent definitions
- `tasks.py` - Task definitions for agents
- `crew.py` - Crew configuration
- `blacklist.py` - Core blacklist management logic
- `data/blacklist.json` - Blacklist data storage

## CrewAI Agents

### Blacklist Management Agents
1. **Blacklist Manager**: Handles CRUD operations on the blacklist
2. **Threat Analyzer**: Analyzes and categorizes threats with risk assessment
3. **Report Generator**: Creates comprehensive reports and summaries
4. **Search Specialist**: Handles complex search queries and pattern matching

### Python Pro Agent
5. **Python Pro - Code Quality Expert**: Modern Python 3.12+ expert for:
   - **Code Review**: Comprehensive reviews with PEP 8, type hints, performance, and security analysis
   - **Code Optimization**: Performance, memory, and readability improvements
   - **Refactoring**: Apply SOLID principles, design patterns, and modern Python features
   - **Testing Strategy**: Design comprehensive test suites with pytest
   - **Modernization**: Upgrade code to Python 3.12+ with async/await, dataclasses, pattern matching, etc.

## Usage

The tool provides an interactive CLI with 15+ operations:

### Blacklist Operations (1-10)
- Add, remove, search, update, and list blacklist entries
- Generate reports and analyze threats
- View statistics and export/import data

### Python Pro Operations (11-15)
- **Option 11**: Review code for quality, performance, and security
- **Option 12**: Optimize code for performance, memory, or readability
- **Option 13**: Refactor code with modern patterns and best practices
- **Option 14**: Create comprehensive testing strategies
- **Option 15**: Modernize legacy code to Python 3.12+

## Example Workflows

### Blacklist Management
```bash
# Add a new threat with AI analysis
1. Select option 1
2. Enter threat details
3. AI analyzes threat level and categorizes it

# Generate a security report
1. Select option 6
2. Choose report type (summary, detailed, statistics)
3. AI generates comprehensive report
```

### Code Quality with Python Pro
```bash
# Review your Python code
1. Select option 11
2. Enter file path (e.g., blacklist.py)
3. Optionally specify focus areas (performance, security, etc.)
4. Receive detailed code review with recommendations

# Modernize legacy code
1. Select option 15
2. Enter file path
3. AI upgrades code to Python 3.12+ with modern features
```
