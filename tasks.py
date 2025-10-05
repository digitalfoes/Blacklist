"""
CrewAI Tasks for Blacklist Management System
"""
from crewai import Task


def create_add_entry_task(agent, entry_data):
    """
    Creates a task to add a new entry to the blacklist.
    
    Args:
        agent: The agent to assign this task to
        entry_data: Dictionary containing entry information (name, reason, threat_level, etc.)
    """
    return Task(
        description=(
            f"Add a new entry to the blacklist with the following information:\n"
            f"Name: {entry_data.get('name', 'Unknown')}\n"
            f"Reason: {entry_data.get('reason', 'Not specified')}\n"
            f"Threat Level: {entry_data.get('threat_level', 'Medium')}\n"
            f"Additional Notes: {entry_data.get('notes', 'None')}\n\n"
            f"Ensure the entry is properly formatted and stored in the blacklist database. "
            f"Validate that the entry doesn't already exist and assign a unique ID."
        ),
        agent=agent,
        expected_output="Confirmation message with the new entry ID and details"
    )


def create_remove_entry_task(agent, identifier):
    """
    Creates a task to remove an entry from the blacklist.
    
    Args:
        agent: The agent to assign this task to
        identifier: ID or name of the entry to remove
    """
    return Task(
        description=(
            f"Remove the blacklist entry identified by: {identifier}\n"
            f"Search for the entry in the database, verify it exists, and remove it. "
            f"Provide confirmation of the removal with details of what was removed."
        ),
        agent=agent,
        expected_output="Confirmation message with details of the removed entry"
    )


def create_search_task(agent, search_query):
    """
    Creates a task to search the blacklist.
    
    Args:
        agent: The agent to assign this task to
        search_query: Search criteria (name, threat level, reason keywords, etc.)
    """
    return Task(
        description=(
            f"Search the blacklist database using the following criteria:\n"
            f"{search_query}\n\n"
            f"Find all matching entries and return them in a structured format. "
            f"If no exact matches are found, suggest similar entries that might be relevant."
        ),
        agent=agent,
        expected_output="List of matching entries with their complete details"
    )


def create_analyze_threat_task(agent, entry_data):
    """
    Creates a task to analyze a threat and provide risk assessment.
    
    Args:
        agent: The agent to assign this task to
        entry_data: Information about the threat to analyze
    """
    return Task(
        description=(
            f"Analyze the following threat information:\n"
            f"Name: {entry_data.get('name', 'Unknown')}\n"
            f"Reason: {entry_data.get('reason', 'Not specified')}\n"
            f"Context: {entry_data.get('context', 'None provided')}\n\n"
            f"Provide a comprehensive threat analysis including:\n"
            f"1. Recommended threat level (Low, Medium, High, Critical)\n"
            f"2. Risk factors and concerns\n"
            f"3. Recommended actions or monitoring strategies\n"
            f"4. Similar threat patterns if any"
        ),
        agent=agent,
        expected_output="Detailed threat analysis report with recommendations"
    )


def create_generate_report_task(agent, report_type="summary"):
    """
    Creates a task to generate a report about the blacklist.
    
    Args:
        agent: The agent to assign this task to
        report_type: Type of report (summary, detailed, statistics, trends)
    """
    return Task(
        description=(
            f"Generate a {report_type} report about the current blacklist status.\n\n"
            f"The report should include:\n"
            f"1. Total number of entries\n"
            f"2. Breakdown by threat level\n"
            f"3. Recent additions (if applicable)\n"
            f"4. Key statistics and trends\n"
            f"5. Notable patterns or concerns\n\n"
            f"Present the information in a clear, organized format that is easy to understand."
        ),
        agent=agent,
        expected_output=f"Comprehensive {report_type} report with statistics and insights"
    )


def create_update_entry_task(agent, identifier, update_data):
    """
    Creates a task to update an existing blacklist entry.
    
    Args:
        agent: The agent to assign this task to
        identifier: ID or name of the entry to update
        update_data: Dictionary containing fields to update
    """
    return Task(
        description=(
            f"Update the blacklist entry identified by: {identifier}\n\n"
            f"Apply the following updates:\n"
            f"{chr(10).join([f'{key}: {value}' for key, value in update_data.items()])}\n\n"
            f"Locate the entry, apply the updates while preserving unchanged fields, "
            f"and confirm the update was successful."
        ),
        agent=agent,
        expected_output="Confirmation message with the updated entry details"
    )


def create_list_all_task(agent, filter_criteria=None):
    """
    Creates a task to list all blacklist entries with optional filtering.
    
    Args:
        agent: The agent to assign this task to
        filter_criteria: Optional filtering criteria (threat level, date range, etc.)
    """
    filter_text = f" matching criteria: {filter_criteria}" if filter_criteria else ""
    
    return Task(
        description=(
            f"Retrieve and list all blacklist entries{filter_text}.\n\n"
            f"Present the entries in a well-organized format showing:\n"
            f"- Entry ID\n"
            f"- Name\n"
            f"- Threat Level\n"
            f"- Reason (summary)\n"
            f"- Date Added\n\n"
            f"Sort the entries by threat level (highest first) and then by date added."
        ),
        agent=agent,
        expected_output="Formatted list of all blacklist entries"
    )


def create_code_review_task(agent, file_path, focus_areas=None):
    """
    Creates a task for the Python Pro agent to review code.
    
    Args:
        agent: The Python Pro agent to assign this task to
        file_path: Path to the file to review
        focus_areas: Optional list of specific areas to focus on
    """
    focus_text = ""
    if focus_areas:
        focus_text = f"\n\nFocus particularly on:\n" + "\n".join([f"- {area}" for area in focus_areas])
    
    return Task(
        description=(
            f"Review the Python code in {file_path} using modern Python 3.12+ best practices.{focus_text}\n\n"
            f"Provide a comprehensive code review covering:\n"
            f"1. Code quality and adherence to PEP 8 and modern Python idioms\n"
            f"2. Type hints and type safety improvements\n"
            f"3. Performance optimization opportunities\n"
            f"4. Error handling and edge cases\n"
            f"5. Security considerations\n"
            f"6. Potential bugs or issues\n"
            f"7. Suggestions for modern Python features (async, dataclasses, pattern matching, etc.)\n"
            f"8. Testing recommendations\n\n"
            f"Provide specific, actionable recommendations with code examples where appropriate."
        ),
        agent=agent,
        expected_output="Detailed code review report with specific recommendations and examples"
    )


def create_code_optimization_task(agent, file_path, optimization_type="performance"):
    """
    Creates a task for the Python Pro agent to optimize code.
    
    Args:
        agent: The Python Pro agent to assign this task to
        file_path: Path to the file to optimize
        optimization_type: Type of optimization (performance, memory, readability, etc.)
    """
    return Task(
        description=(
            f"Optimize the Python code in {file_path} focusing on {optimization_type}.\n\n"
            f"Analyze the code and provide optimizations for:\n"
            f"1. {optimization_type.capitalize()} improvements\n"
            f"2. Modern Python 3.12+ features that could improve the code\n"
            f"3. Better algorithms or data structures if applicable\n"
            f"4. Async/await patterns for I/O-bound operations\n"
            f"5. Caching strategies where beneficial\n"
            f"6. Memory efficiency improvements\n\n"
            f"Provide before/after code examples showing the improvements and explain "
            f"the benefits of each optimization."
        ),
        agent=agent,
        expected_output="Optimization report with specific code improvements and performance analysis"
    )


def create_refactoring_task(agent, file_path, refactoring_goals):
    """
    Creates a task for the Python Pro agent to refactor code.
    
    Args:
        agent: The Python Pro agent to assign this task to
        file_path: Path to the file to refactor
        refactoring_goals: List of refactoring goals or patterns to apply
    """
    goals_text = "\n".join([f"- {goal}" for goal in refactoring_goals])
    
    return Task(
        description=(
            f"Refactor the Python code in {file_path} to achieve the following goals:\n"
            f"{goals_text}\n\n"
            f"Apply modern Python best practices including:\n"
            f"1. SOLID principles and design patterns\n"
            f"2. Type hints and Pydantic models for data validation\n"
            f"3. Proper error handling with custom exceptions\n"
            f"4. Dataclasses or Pydantic models instead of plain dicts where appropriate\n"
            f"5. Context managers for resource management\n"
            f"6. Modern Python idioms and features\n\n"
            f"Provide the refactored code with explanations of the changes and their benefits."
        ),
        agent=agent,
        expected_output="Refactored code with detailed explanations of improvements"
    )


def create_testing_strategy_task(agent, file_path):
    """
    Creates a task for the Python Pro agent to design a testing strategy.
    
    Args:
        agent: The Python Pro agent to assign this task to
        file_path: Path to the file to create tests for
    """
    return Task(
        description=(
            f"Design a comprehensive testing strategy for the code in {file_path}.\n\n"
            f"Create a testing plan that includes:\n"
            f"1. Unit tests with pytest covering all functions and methods\n"
            f"2. Test fixtures and factories for test data\n"
            f"3. Parametrized tests for multiple scenarios\n"
            f"4. Mock objects for external dependencies\n"
            f"5. Edge cases and error conditions\n"
            f"6. Integration tests if applicable\n"
            f"7. Property-based tests with Hypothesis for complex logic\n"
            f"8. Coverage goals and recommendations\n\n"
            f"Provide example test code using modern pytest features and best practices."
        ),
        agent=agent,
        expected_output="Comprehensive testing strategy with example test code"
    )


def create_modernization_task(agent, file_path):
    """
    Creates a task for the Python Pro agent to modernize legacy code.
    
    Args:
        agent: The Python Pro agent to assign this task to
        file_path: Path to the file to modernize
    """
    return Task(
        description=(
            f"Modernize the Python code in {file_path} to use Python 3.12+ features and best practices.\n\n"
            f"Update the code to leverage:\n"
            f"1. Modern type hints including generics and Protocol typing\n"
            f"2. Dataclasses or Pydantic models for data structures\n"
            f"3. Pattern matching (match statements) where appropriate\n"
            f"4. Async/await for I/O operations\n"
            f"5. Context managers and proper resource management\n"
            f"6. Modern string formatting (f-strings)\n"
            f"7. Pathlib instead of os.path\n"
            f"8. Modern standard library features\n\n"
            f"Provide the modernized code with explanations of the improvements and migration notes."
        ),
        agent=agent,
        expected_output="Modernized code with migration guide and explanations"
    )
