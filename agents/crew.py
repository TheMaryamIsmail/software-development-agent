import os
from crewai import Agent, Crew, Process, Task, LLM
from dotenv import load_dotenv
from agents.tools import save_artifact

load_dotenv()

# Initialize Gemini LLM for CrewAI
gemini_llm = LLM(
    model=os.getenv("GEMINI_MODEL","gemini-3.8-flash"),
    api_key=os.getenv("GEMINI_API_KEY")
)

class SoftwareDevCrew:
    def __init__(self, requirement: str):
        self.requirement = requirement

    async def run(self):
        # --- Define Agents using Gemini LLM ---
        planner = Agent(
            role='Technical Project Manager',
            goal='Analyze software requirements and produce a clear, step-by-step implementation plan.',
            backstory='Expert in system architecture and technical scoping, translating product requirements into engineering roadmaps.',
            verbose=True,
            tools=[save_artifact],
            llm=gemini_llm
        )

        coder = Agent(
            role='Senior Python Developer',
            goal='Write robust, clean, and production-ready Python code based on the implementation plan.',
            backstory='Master Python developer who writes modular, well-documented, and efficient code following best practices.',
            verbose=True,
            tools=[save_artifact],
            llm=gemini_llm
        )

        tester = Agent(
            role='QA Automation Engineer',
            goal='Create comprehensive unit test cases using unittest for the generated code.',
            backstory='Meticulous quality assurance specialist skilled in edge-case testing, test automation, and validation.',
            verbose=True,
            tools=[save_artifact],
            llm=gemini_llm
        )

        reviewer = Agent(
            role='Code Reviewer & Security Expert',
            goal='Review the code and test cases, identify potential bugs, security vulnerabilities, and code smells.',
            backstory='Strict code reviewer with deep knowledge of secure coding standards, performance bottlenecks, and design patterns.',
            verbose=True,
            tools=[save_artifact],
            llm=gemini_llm
        )

        reporter = Agent(
            role='DevOps & Documentation Specialist',
            goal='Produce the final code integration summary and a professional development report.',
            backstory='Technical writer and release manager skilled at compiling technical metrics, code summaries, and final status reports.',
            verbose=True,
            tools=[save_artifact],
            llm=gemini_llm
        )

        # Tasks and Crew workflow remain the same...
        plan_task = Task(
            description=f"Analyze the following requirement: '{self.requirement}'. Create an implementation plan detailing data structures, functions, and modules needed.",
            expected_output="A Markdown document outlining the implementation plan, saved using the save_artifact tool as 'implementation_plan.md'.",
            agent=planner
        )

        code_task = Task(
            description="Using the implementation plan, write the complete, executable Python code required to fulfill the user requirement.",
            expected_output="Python source code saved using the save_artifact tool as 'generated_code.py'.",
            agent=coder
        )

        test_task = Task(
            description="Write a comprehensive suite of unit tests for the generated Python code using the `unittest` framework.",
            expected_output="Python test script saved using the save_artifact tool as 'test_cases.py'.",
            agent=tester
        )

        review_task = Task(
            description="Review the generated code and test cases for bugs, security issues, and style violations. Suggest specific improvements if any.",
            expected_output="A Markdown review report saved using the save_artifact tool as 'code_review.md'.",
            agent=reviewer
        )

        report_task = Task(
            description="Compile all generated artifacts (Plan, Code, Tests, Review) into a final cohesive development report summarizing the project status.",
            expected_output="A final Markdown development report saved using the save_artifact tool as 'development_report.md'.",
            agent=reporter
        )

        dev_crew = Crew(
            agents=[planner, coder, tester, reviewer, reporter],
            tasks=[plan_task, code_task, test_task, review_task, report_task],
            process=Process.sequential,
            verbose=True
        )

        return await dev_crew.kickoff_async()