import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from agents.crew import SoftwareDevCrew

app = FastAPI(title="AI Software Development Team")

# Setup Jinja2 templates directory
templates = Jinja2Templates(directory="templates")

class RequirementRequest(BaseModel):
    requirement: str

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    # Render the Jinja2 template with context data
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request, "title": "AI Software Development Team"},
    )

@app.post("/api/run")
async def run_crew(payload: RequirementRequest):
    requirement = payload.requirement.strip()
    if not requirement:
        raise HTTPException(status_code=400, detail="Requirement cannot be empty")

    try:
        # Run CrewAI workflow synchronously 
        crew = SoftwareDevCrew(requirement)
        await crew.run()

        # Read generated artifacts back to send to frontend
        artifacts = {}
        output_dir = "output"
        if os.path.exists(output_dir):
            for filename in os.listdir(output_dir):
                filepath = os.path.join(output_dir, filename)
                if os.path.isfile(filepath):
                    with open(filepath, "r", encoding="utf-8") as f:
                        artifacts[filename] = f.read()

        return {"success": True, "artifacts": artifacts}
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)