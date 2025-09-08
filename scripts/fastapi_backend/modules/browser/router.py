"""
Browser automation module router
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
import asyncio
from playwright.async_api import async_playwright

from core.database import get_db
from modules.auth.router import get_current_user
from .schemas import BrowserTaskCreate, BrowserTaskResponse, ScreenshotRequest
from .models import BrowserSession, BrowserTask
from .services import BrowserAutomationService

router = APIRouter()

@router.post("/sessions", response_model=dict)
async def create_browser_session(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Create a new browser session"""
    session = BrowserSession(
        user_id=current_user.id,
        status="active"
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    
    return {
        "session_id": session.id,
        "status": session.status,
        "created_at": session.created_at
    }

@router.post("/tasks", response_model=BrowserTaskResponse)
async def create_browser_task(
    task_data: BrowserTaskCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Create and execute a browser automation task"""
    
    # Create task record
    task = BrowserTask(
        user_id=current_user.id,
        session_id=task_data.session_id,
        task_type=task_data.task_type,
        instructions=task_data.instructions,
        status="pending"
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    
    # Execute task in background
    automation_service = BrowserAutomationService()
    background_tasks.add_task(
        automation_service.execute_task,
        task.id,
        task_data.instructions,
        db
    )
    
    return BrowserTaskResponse(
        task_id=task.id,
        status=task.status,
        task_type=task.task_type,
        created_at=task.created_at
    )

@router.post("/screenshot")
async def take_screenshot(
    request: ScreenshotRequest,
    current_user = Depends(get_current_user)
):
    """Take a screenshot of a webpage"""
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        try:
            await page.goto(request.url)
            await page.wait_for_load_state("networkidle")
            
            screenshot = await page.screenshot(
                full_page=request.full_page,
                type="png"
            )
            
            return {
                "success": True,
                "screenshot_size": len(screenshot),
                "url": request.url
            }
            
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Screenshot failed: {str(e)}")
        
        finally:
            await browser.close()

@router.get("/tasks/{task_id}", response_model=BrowserTaskResponse)
async def get_task_status(
    task_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get browser task status and results"""
    
    task = db.query(BrowserTask).filter(
        BrowserTask.id == task_id,
        BrowserTask.user_id == current_user.id
    ).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return BrowserTaskResponse(
        task_id=task.id,
        status=task.status,
        task_type=task.task_type,
        result=task.result,
        created_at=task.created_at,
        completed_at=task.completed_at
    )
