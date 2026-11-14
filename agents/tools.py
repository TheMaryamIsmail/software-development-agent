import os
from crewai.tools import tool

@tool("Save Artifact to File")
def save_artifact(filename: str, content: str) -> str:
    """Saves the generated code, plan, test cases, or reports into the output directory."""
    os.makedirs("output", exist_ok=True)
    filepath = os.path.join("output", filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    return f"Successfully saved {filename} to output folder."