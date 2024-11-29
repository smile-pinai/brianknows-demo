from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os
from dotenv import load_dotenv
from typing import Dict, List, Optional
from pydantic import BaseModel
import uvicorn

# 加载环境变量
load_dotenv()

app = FastAPI(title="BrianKnows API Integration")

# CORS设置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API基础URL
BASE_URL = "https://api.brianknows.org"
API_KEY = os.getenv("BRIANKNOWS_API_KEY")

# 请求头设置
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Pydantic模型
class Agent(BaseModel):
    name: str
    description: Optional[str] = None
    knowledge_base_ids: List[str]

class KnowledgeBase(BaseModel):
    name: str
    description: Optional[str] = None

@app.get("/agents", response_model=List[Dict])
async def get_agents():
    """获取所有agents"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/agents", headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        return response.json()

@app.post("/agents")
async def create_agent(agent: Agent):
    """创建新agent"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/agents",
            headers=headers,
            json=agent.dict()
        )
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        return response.json()

@app.get("/knowledge-bases", response_model=List[Dict])
async def get_knowledge_bases():
    """获取所有knowledge bases"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/knowledge-bases", headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        return response.json()

@app.post("/knowledge-bases")
async def create_knowledge_base(kb: KnowledgeBase):
    """创建新knowledge base"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/knowledge-bases",
            headers=headers,
            json=kb.dict()
        )
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        return response.json()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 