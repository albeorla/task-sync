import os
from datetime import datetime

from crewai import Agent, Crew, Process, Task
from crewai.tasks.task_output import TaskOutput
from dotenv import load_dotenv
from langchain.tools import DuckDuckGoSearchRun, ReadFileTool, WriteFileTool
from loguru import logger

load_dotenv()


def write_file(directory: str, filename: str, data: str) -> None:
    """Write data to a file. Supported are .json, .csv and .txt files."""
    try:
        with open(os.path.join(directory, filename), "w") as file:
            file.write(data)
    except OSError as error:
        logger.error(f"Error writing file {filename}: {error}")
        raise


def create_directory(path: str) -> None:
    """Create a directory if it doesn't exist."""
    try:
        os.makedirs(path, exist_ok=True)
    except OSError as error:
        logger.error(f"Error creating directory {path}: {error}")
        raise


def get_agents():
    """
    Returns a list of agents (each agent is an Agent object).
    :return: a list of agents (each agent is an Agent object)
    """

    # Define agents
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

    return [
        api_integration_developer_agent,
        workflow_designer_agent
    ]


def get_tasks(api_integration_developer_agent, workflow_designer_agent):
    """
    Returns a list of tasks. Each task is a list of Task objects.
    :param api_integration_developer_agent: an Agent object that represents the API Integration Developer
    :param workflow_designer_agent: an Agent object that represents the Workflow Designer
    :return: a list of task where each task is a Task object
    """

    # Define tools for each task
    tools = [
        DuckDuckGoSearchRun(),
        WriteFileTool(),
        ReadFileTool()
    ]

    # Define tasks
    api_integration_task = Task(
        description="Develop API connectors for Google Calendar, Todoist, and Notion",
        agent=api_integration_developer_agent,
        tools=tools,
        output=TaskOutput(
            description="""
                    Create robust API connectors using Python to interact with Google Calendar, Todoist, and Notion APIs.
                    Authenticate using API keys and manage data flow between these platforms. 
                    Handle synchronization issues with proper error logging.
                """,
            result="""
                    API connectors are successfully developed and functional, ensuring seamless data exchange and synchronization.
                    Write output to a local file.
                """
        )
    )

    workflow_designer_task = Task(
        description="Design and implement the workflow management system",
        agent=workflow_designer_agent,
        tools=tools,
        output=TaskOutput(
            description="""
                    Develop a system to organize projects, tasks, and resources in a hierarchical structure. 
                    Design algorithms for task allocation and scheduling in Google Calendar, 
                    and create mechanisms to identify and resolve overlaps and redundancies.
                """,
            result="""
                    A comprehensive workflow management system is established, enhancing efficiency and coordination across platforms.
                    Write output to a local file.
                """
        )
    )

    return [
        api_integration_task,
        workflow_designer_task
    ]


def get_crew(agents, tasks):
    """
    Returns a parameterized Crew object.
    :param agents:  A list of Agent objects
    :param tasks:  A list of Task objects
    :return: A Crew object
    """
    return Crew(
        agents=agents,
        tasks=tasks,
        process=Process.sequential,
    )


def write_result_file(crew, result):
    directory = "crew_output"
    filename = f"{crew.id}-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.json"
    create_directory(directory)
    write_file(directory, filename, result)


def main():
    agents = get_agents()
    tasks = get_tasks(*agents)
    crew = get_crew(agents, tasks)
    result = crew.kickoff()
    write_result_file(crew, result)


if __name__ == '__main__':
    main()
