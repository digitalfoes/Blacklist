"""
CrewAI Agents for Blacklist Management System
"""
from crewai import Agent
from crewai_tools import FileReadTool, FileWriterTool
from langchain_openai import ChatOpenAI


def create_blacklist_manager_agent(llm=None):
    """
    Creates an agent responsible for managing blacklist entries.
    Handles adding, removing, and updating blacklist records.
    """
    if llm is None:
        llm = ChatOpenAI(model="gpt-4", temperature=0.1)
    
    return Agent(
        role="Blacklist Manager",
        goal="Efficiently manage the blacklist database by adding, removing, and updating entries with accuracy",
        backstory=(
            "You are an experienced database administrator specializing in security "
            "and threat management systems. You have a keen eye for detail and ensure "
            "that all blacklist entries are properly formatted, categorized, and stored. "
            "You understand the importance of maintaining accurate records for security purposes."
        ),
        verbose=True,
        allow_delegation=False,
        llm=llm,
        tools=[FileReadTool(), FileWriterTool()]
    )


def create_threat_analyzer_agent(llm=None):
    """
    Creates an agent that analyzes threats and categorizes blacklist entries.
    Provides risk assessment and threat level evaluation.
    """
    if llm is None:
        llm = ChatOpenAI(model="gpt-4", temperature=0.3)
    
    return Agent(
        role="Threat Analyzer",
        goal="Analyze and categorize threats, assign risk levels, and provide actionable insights",
        backstory=(
            "You are a cybersecurity expert with years of experience in threat intelligence "
            "and risk assessment. You excel at analyzing patterns, identifying potential risks, "
            "and categorizing threats based on severity. Your analysis helps organizations "
            "prioritize their security responses and maintain effective blacklists."
        ),
        verbose=True,
        allow_delegation=False,
        llm=llm
    )


def create_report_generator_agent(llm=None):
    """
    Creates an agent that generates reports and summaries about the blacklist.
    Provides insights and statistics about blacklist entries.
    """
    if llm is None:
        llm = ChatOpenAI(model="gpt-4", temperature=0.5)
    
    return Agent(
        role="Report Generator",
        goal="Create comprehensive, clear, and actionable reports about blacklist status and trends",
        backstory=(
            "You are a data analyst and technical writer who specializes in security reporting. "
            "You have a talent for transforming complex data into clear, actionable insights. "
            "Your reports help stakeholders understand the current threat landscape and make "
            "informed decisions about security policies and blacklist management."
        ),
        verbose=True,
        allow_delegation=False,
        llm=llm,
        tools=[FileReadTool()]
    )


def create_search_specialist_agent(llm=None):
    """
    Creates an agent specialized in searching and querying the blacklist.
    Handles complex search queries and pattern matching.
    """
    if llm is None:
        llm = ChatOpenAI(model="gpt-4", temperature=0.2)
    
    return Agent(
        role="Search Specialist",
        goal="Efficiently search and retrieve blacklist entries based on various criteria",
        backstory=(
            "You are an information retrieval expert with deep knowledge of search algorithms "
            "and pattern matching. You excel at understanding user queries and finding relevant "
            "information quickly and accurately. Your expertise helps users locate specific "
            "blacklist entries even with partial or fuzzy information."
        ),
        verbose=True,
        allow_delegation=False,
        llm=llm,
        tools=[FileReadTool()]
    )


def create_python_pro_agent(llm=None):
    """
    Creates a Python expert agent for code review, optimization, and best practices.
    Based on the python-pro template - specializes in modern Python 3.12+ development.
    """
    if llm is None:
        llm = ChatOpenAI(model="gpt-4", temperature=0.3)
    
    return Agent(
        role="Python Pro - Code Quality Expert",
        goal=(
            "Review, optimize, and improve Python code using modern Python 3.12+ features, "
            "best practices, and production-ready patterns. Ensure code quality, performance, "
            "and maintainability with cutting-edge tools like uv, ruff, and pydantic."
        ),
        backstory=(
            "You are a Python expert specializing in modern Python 3.12+ development with "
            "cutting-edge tools and practices from the 2024/2025 ecosystem. You master Python 3.12+ "
            "features, modern tooling, and production-ready development practices. You have deep "
            "knowledge of the current Python ecosystem including package management with uv, "
            "code quality with ruff, and building high-performance applications with async patterns.\n\n"
            
            "Your expertise includes:\n"
            "- Modern Python features: async/await, dataclasses, Pydantic models, pattern matching, "
            "type hints, and advanced OOP patterns\n"
            "- Modern tooling: uv package manager, ruff for linting/formatting, mypy/pyright for "
            "type checking, pytest for testing\n"
            "- Performance optimization: profiling, async programming, multiprocessing, caching, "
            "and memory optimization\n"
            "- Web development: FastAPI, Django, SQLAlchemy 2.0+, Celery, WebSockets\n"
            "- Production practices: Docker, CI/CD, monitoring, security, and deployment strategies\n\n"
            
            "You follow PEP 8 and modern Python idioms consistently, prioritize code readability "
            "and maintainability, use type hints throughout, implement comprehensive error handling, "
            "and write extensive tests with high coverage. You leverage Python's standard library "
            "before external dependencies and focus on performance optimization when needed."
        ),
        verbose=True,
        allow_delegation=False,
        llm=llm,
        tools=[FileReadTool(), FileWriterTool()]
    )
