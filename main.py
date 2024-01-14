from crewai import Agent, Crew, Process, Task
from crewai.tasks.task_output import TaskOutput
from dotenv import load_dotenv
from langchain.tools import DuckDuckGoSearchRun

load_dotenv()


def main():
    # Agents
    api_integration_developer_agent = Agent(
        role="API Integration Developer",
        goal="Develop and manage API connectors and data synchronization for Google Calendar, Todoist, and Notion",
        backstory="""
            A software engineer skilled in developing robust API connectors and handling data synchronization 
            between multiple platforms like Google Calendar, Todoist, and Notion. Their expertise ensures seamless 
            data flow and integrity across these services.
        """,
        memory=True,
        verbose=True,
        allow_delegation=True
    )

    workflow_designer_agent = Agent(
        role="Workflow Designer",
        goal="Design and manage the workflow management system",
        backstory="""
            A specialist in designing efficient, effective, and scalable workflow management systems. 
            They are responsible for structuring project hierarchies, task allocation, and resolving overlaps 
            and redundancies in task management across various platforms.
        """,
        memory=True,
        verbose=True,
        allow_delegation=True
    )

    # Tasks for API Integration Developer
    search_tool = DuckDuckGoSearchRun()
    api_integration_tasks = [
        Task(
            description="Develop API connectors for Google Calendar, Todoist, and Notion",
            agent=api_integration_developer_agent,
            tools=[search_tool],
            output=TaskOutput(
                description="""
                    Create robust API connectors using Python to interact with Google Calendar, Todoist, and Notion APIs.
                    Authenticate using API keys and manage data flow between these platforms. 
                    Handle synchronization issues with proper error logging.
                """,
                result="""
                    API connectors are successfully developed and functional, ensuring seamless data exchange and synchronization.
                """
            )
        )
    ]

    # Tasks for Workflow Designer
    workflow_designer_tasks = [
        Task(
            description="Design and implement the workflow management system",
            agent=workflow_designer_agent,
            tools=[search_tool],
            output=TaskOutput(
                description="""
                    Develop a system to organize projects, tasks, and resources in a hierarchical structure. 
                    Design algorithms for task allocation and scheduling in Google Calendar, 
                    and create mechanisms to identify and resolve overlaps and redundancies.
                """,
                result="""
                    A comprehensive workflow management system is established, enhancing efficiency and coordination across platforms.
                """
            )
        )
    ]

    # Crew assembly
    crew = Crew(
        agents=[
            api_integration_developer_agent,
            workflow_designer_agent
        ],
        tasks=api_integration_tasks + workflow_designer_tasks,
        process=Process.sequential,
    )
    crew.kickoff()


if __name__ == '__main__':
    main()
