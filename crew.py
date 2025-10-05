"""
CrewAI Crew Configuration for Blacklist Management System
"""
from crewai import Crew, Process
from agents import (
    create_blacklist_manager_agent,
    create_threat_analyzer_agent,
    create_report_generator_agent,
    create_search_specialist_agent,
    create_python_pro_agent
)
from tasks import (
    create_add_entry_task,
    create_remove_entry_task,
    create_search_task,
    create_analyze_threat_task,
    create_generate_report_task,
    create_update_entry_task,
    create_list_all_task,
    create_code_review_task,
    create_code_optimization_task,
    create_refactoring_task,
    create_testing_strategy_task,
    create_modernization_task
)


class BlacklistCrew:
    """
    Main crew orchestrator for the blacklist management system.
    Coordinates multiple agents to handle various blacklist operations.
    """
    
    def __init__(self, llm=None):
        """
        Initialize the BlacklistCrew with agents.
        
        Args:
            llm: Optional language model to use for all agents
        """
        self.llm = llm
        self.manager_agent = create_blacklist_manager_agent(llm)
        self.analyzer_agent = create_threat_analyzer_agent(llm)
        self.reporter_agent = create_report_generator_agent(llm)
        self.search_agent = create_search_specialist_agent(llm)
        self.python_pro_agent = create_python_pro_agent(llm)
    
    def add_entry(self, entry_data):
        """
        Add a new entry to the blacklist with threat analysis.
        
        Args:
            entry_data: Dictionary containing entry information
        
        Returns:
            Result of the crew execution
        """
        # First analyze the threat
        analyze_task = create_analyze_threat_task(self.analyzer_agent, entry_data)
        
        # Then add the entry with the analysis
        add_task = create_add_entry_task(self.manager_agent, entry_data)
        add_task.context = [analyze_task]
        
        crew = Crew(
            agents=[self.analyzer_agent, self.manager_agent],
            tasks=[analyze_task, add_task],
            process=Process.sequential,
            verbose=True
        )
        
        return crew.kickoff()
    
    def remove_entry(self, identifier):
        """
        Remove an entry from the blacklist.
        
        Args:
            identifier: ID or name of the entry to remove
        
        Returns:
            Result of the crew execution
        """
        remove_task = create_remove_entry_task(self.manager_agent, identifier)
        
        crew = Crew(
            agents=[self.manager_agent],
            tasks=[remove_task],
            process=Process.sequential,
            verbose=True
        )
        
        return crew.kickoff()
    
    def search_entries(self, search_query):
        """
        Search for entries in the blacklist.
        
        Args:
            search_query: Search criteria
        
        Returns:
            Result of the crew execution
        """
        search_task = create_search_task(self.search_agent, search_query)
        
        crew = Crew(
            agents=[self.search_agent],
            tasks=[search_task],
            process=Process.sequential,
            verbose=True
        )
        
        return crew.kickoff()
    
    def update_entry(self, identifier, update_data):
        """
        Update an existing blacklist entry.
        
        Args:
            identifier: ID or name of the entry to update
            update_data: Dictionary containing fields to update
        
        Returns:
            Result of the crew execution
        """
        update_task = create_update_entry_task(self.manager_agent, identifier, update_data)
        
        crew = Crew(
            agents=[self.manager_agent],
            tasks=[update_task],
            process=Process.sequential,
            verbose=True
        )
        
        return crew.kickoff()
    
    def generate_report(self, report_type="summary"):
        """
        Generate a report about the blacklist.
        
        Args:
            report_type: Type of report to generate
        
        Returns:
            Result of the crew execution
        """
        report_task = create_generate_report_task(self.reporter_agent, report_type)
        
        crew = Crew(
            agents=[self.reporter_agent],
            tasks=[report_task],
            process=Process.sequential,
            verbose=True
        )
        
        return crew.kickoff()
    
    def list_all_entries(self, filter_criteria=None):
        """
        List all blacklist entries with optional filtering.
        
        Args:
            filter_criteria: Optional filtering criteria
        
        Returns:
            Result of the crew execution
        """
        list_task = create_list_all_task(self.search_agent, filter_criteria)
        
        crew = Crew(
            agents=[self.search_agent],
            tasks=[list_task],
            process=Process.sequential,
            verbose=True
        )
        
        return crew.kickoff()
    
    def analyze_threat(self, entry_data):
        """
        Analyze a threat without adding it to the blacklist.
        
        Args:
            entry_data: Information about the threat
        
        Returns:
            Result of the crew execution
        """
        analyze_task = create_analyze_threat_task(self.analyzer_agent, entry_data)
        
        crew = Crew(
            agents=[self.analyzer_agent],
            tasks=[analyze_task],
            process=Process.sequential,
            verbose=True
        )
        
        return crew.kickoff()
    
    def review_code(self, file_path, focus_areas=None):
        """
        Review Python code using the Python Pro agent.
        
        Args:
            file_path: Path to the file to review
            focus_areas: Optional list of specific areas to focus on
        
        Returns:
            Result of the crew execution
        """
        review_task = create_code_review_task(self.python_pro_agent, file_path, focus_areas)
        
        crew = Crew(
            agents=[self.python_pro_agent],
            tasks=[review_task],
            process=Process.sequential,
            verbose=True
        )
        
        return crew.kickoff()
    
    def optimize_code(self, file_path, optimization_type="performance"):
        """
        Optimize Python code using the Python Pro agent.
        
        Args:
            file_path: Path to the file to optimize
            optimization_type: Type of optimization (performance, memory, readability)
        
        Returns:
            Result of the crew execution
        """
        optimize_task = create_code_optimization_task(self.python_pro_agent, file_path, optimization_type)
        
        crew = Crew(
            agents=[self.python_pro_agent],
            tasks=[optimize_task],
            process=Process.sequential,
            verbose=True
        )
        
        return crew.kickoff()
    
    def refactor_code(self, file_path, refactoring_goals):
        """
        Refactor Python code using the Python Pro agent.
        
        Args:
            file_path: Path to the file to refactor
            refactoring_goals: List of refactoring goals
        
        Returns:
            Result of the crew execution
        """
        refactor_task = create_refactoring_task(self.python_pro_agent, file_path, refactoring_goals)
        
        crew = Crew(
            agents=[self.python_pro_agent],
            tasks=[refactor_task],
            process=Process.sequential,
            verbose=True
        )
        
        return crew.kickoff()
    
    def create_testing_strategy(self, file_path):
        """
        Create a testing strategy using the Python Pro agent.
        
        Args:
            file_path: Path to the file to create tests for
        
        Returns:
            Result of the crew execution
        """
        testing_task = create_testing_strategy_task(self.python_pro_agent, file_path)
        
        crew = Crew(
            agents=[self.python_pro_agent],
            tasks=[testing_task],
            process=Process.sequential,
            verbose=True
        )
        
        return crew.kickoff()
    
    def modernize_code(self, file_path):
        """
        Modernize Python code to use Python 3.12+ features.
        
        Args:
            file_path: Path to the file to modernize
        
        Returns:
            Result of the crew execution
        """
        modernize_task = create_modernization_task(self.python_pro_agent, file_path)
        
        crew = Crew(
            agents=[self.python_pro_agent],
            tasks=[modernize_task],
            process=Process.sequential,
            verbose=True
        )
        
        return crew.kickoff()
