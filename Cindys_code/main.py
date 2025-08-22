import os 
from fastapi import FastAPI, Request, HTTPException 
from fastapi.responses import HTMLResponse, JSONResponse 
from fastapi.templating import Jinja2Templates 
from fastapi.staticfiles import StaticFiles 
from pydantic import BaseModel 
from dotenv import load_dotenv 
from starlette.middleware.cors import CORSMiddleware # For allowing frontend to access API 
from openinference.instrumentation.beeai import BeeAIInstrumentor 
 
from agent import run_faq_agent, _setup_rag_system, get_observability_data 
import time # Added for observability endpoint
 
load_dotenv() 
 
app = FastAPI( 
    title="Company FAQ RAG API", 
    description="Backend API for the Company FAQ Retrieval Augmented Generation (RAG) system.", 
    version="1.0.0", 
) 
 
origins = [ 
    "http://localhost", 
    "http://localhost:8000", 
    "http://127.0.0.1:8080", 
    "http://0.0.0.0:8000", 
    "http://localhost:8001", 
] 
 
app.add_middleware( 
    CORSMiddleware, 
    allow_origins=origins, 
    allow_credentials=True, 
    allow_methods=["*"], 
    allow_headers=["*"], 
) 
 
 
app.mount( 
    "/static", 
    StaticFiles(directory="frontend/static"), 
    name="static" 
) 
templates = Jinja2Templates(directory="./frontend") 
 
 
 
class ChatRequest(BaseModel): 
    query: str 
 
class ChatResponse(BaseModel): 
    answer: str 
 
 
@app.on_event("startup") 
async def startup_event(): 
    """Initializes the RAG system when the FastAPI app starts up.""" 
    print("FastAPI startup event: Initializing RAG system...") 
    success = _setup_rag_system() 
    if not success: 
        print("RAG system initialization failed during startup.") 
    else: 
        print("RAG system initialized successfully.") 
    BeeAIInstrumentor().instrument() 
 
 
@app.get("/", response_class=HTMLResponse) 
async def serve_frontend(request: Request): 
    """Serve the main HTML page for the frontend.""" 
    return templates.TemplateResponse("index.html", {"request": request}) 
 
@app.post("/chat", response_model=ChatResponse) 
async def chat_endpoint(request_body: ChatRequest): 
    """ 
    Endpoint for user queries. 
    Passes the query to the RAG agent and returns the response. 
    """ 
    user_query = request_body.query 
    print(f"Received query: {user_query}") 
    try: 
        agent_answer = await run_faq_agent(user_query) 
        return ChatResponse(answer=agent_answer) 
    except Exception as e: 
        print(f"Error processing chat request: {e}") 
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}") 

@app.get("/observability")
async def observability_endpoint():
    """
    Endpoint for system observability and health monitoring.
    Returns detailed information about the RAG system components and OpenTelemetry status.
    """
    try:
        obs_data = get_observability_data()
        return {
            "status": "success",
            "timestamp": time.time(),
            "data": obs_data
        }
    except Exception as e:
        print(f"Error getting observability data: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving observability data: {e}")

if __name__ == "__main__": 
    import uvicorn 
    port = 8001 
    # port = int(os.environ.get("PORT", 8001)) 
    uvicorn.run("main:app", host="127.0.0.1", port=port, reload=True) 
