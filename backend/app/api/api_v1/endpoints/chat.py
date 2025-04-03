from typing import Any, List, Dict
import json
import asyncio

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

# 使用OpenAI官方Agents SDK
from openai.types.responses import ResponseTextDeltaEvent
from agents import Agent, Runner

from app import crud, models, schemas
from app.api import deps
from app.config import settings

router = APIRouter()


@router.get("/{agent_id}/history", response_model=List[schemas.ChatMessage])
def read_chat_history(
    *,
    db: Session = Depends(deps.get_db),
    agent_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    获取与特定Agent的聊天历史
    """
    # 检查Agent是否存在和权限
    agent = crud.agent.get(db=db, id=agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent不存在")
    if not current_user.is_admin and (agent.user_id != current_user.id):
        raise HTTPException(status_code=400, detail="没有足够的权限")
    
    # 获取聊天历史
    chat_messages = crud.chat_message.get_by_agent_and_user(
        db=db,
        agent_id=agent_id,
        user_id=current_user.id,
        skip=skip,
        limit=limit,
    )
    return chat_messages


@router.post("/{agent_id}/send", response_model=schemas.ChatMessage)
async def send_message(
    *,
    db: Session = Depends(deps.get_db),
    agent_id: int,
    message: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    向Agent发送消息并获取响应
    """
    # 检查Agent是否存在和权限
    agent_db = crud.agent.get(db=db, id=agent_id)
    if not agent_db:
        raise HTTPException(status_code=404, detail="Agent不存在")
    if not current_user.is_admin and (agent_db.user_id != current_user.id):
        raise HTTPException(status_code=400, detail="没有足够的权限")
    
    # 创建用户消息记录
    user_message = crud.chat_message.create(
        db=db,
        obj_in=schemas.ChatMessageCreate(
            role="user",
            content=message,
            agent_id=agent_id,
            user_id=current_user.id,
        ),
    )
    
    # 使用OpenAI Agents SDK获取响应
    try:
        # 获取最近的10条聊天记录作为上下文
        chat_history = crud.chat_message.get_by_agent_and_user(
            db=db,
            agent_id=agent_id,
            user_id=current_user.id,
            skip=0,
            limit=10,
        )
        
        # 构建消息历史
        messages = []
        for chat in reversed(chat_history):
            messages.append({"role": chat.role, "content": chat.content})
        
        # 创建Agent配置和实例
        agent = Agent(
            name=agent_db.name,
            instructions=agent_db.instructions or "你是一个有用的AI助手。",
            model="gpt-3.5-turbo",
        )
        
        # 运行Agent
        result = await Runner.run(
            agent,
            input=message,
            context={"messages": messages}
        )
        
        # 提取助手回复
        assistant_message_content = result.output
        
        # 创建助手消息记录
        assistant_message = crud.chat_message.create(
            db=db,
            obj_in=schemas.ChatMessageCreate(
                role="assistant",
                content=assistant_message_content,
                agent_id=agent_id,
                user_id=current_user.id,
            ),
        )
        
        return assistant_message
    except Exception as e:
        # 记录错误并返回错误消息
        error_message = f"处理消息时出错: {str(e)}"
        assistant_message = crud.chat_message.create(
            db=db,
            obj_in=schemas.ChatMessageCreate(
                role="assistant",
                content=error_message,
                agent_id=agent_id,
                user_id=current_user.id,
            ),
        )
        return assistant_message


@router.post("/{agent_id}/stream")
async def stream_chat(
    *,
    db: Session = Depends(deps.get_db),
    background_tasks: BackgroundTasks,
    agent_id: int,
    message: str,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    流式聊天接口，支持实时返回
    """
    # 检查Agent是否存在和权限
    agent_db = crud.agent.get(db=db, id=agent_id)
    if not agent_db:
        raise HTTPException(status_code=404, detail="Agent不存在")
    if not current_user.is_admin and (agent_db.user_id != current_user.id):
        raise HTTPException(status_code=400, detail="没有足够的权限")
    
    # 创建用户消息记录
    user_message = crud.chat_message.create(
        db=db,
        obj_in=schemas.ChatMessageCreate(
            role="user",
            content=message,
            agent_id=agent_id,
            user_id=current_user.id,
        ),
    )
    
    # 获取最近的10条聊天记录作为上下文
    chat_history = crud.chat_message.get_by_agent_and_user(
        db=db,
        agent_id=agent_id,
        user_id=current_user.id,
        skip=0,
        limit=10,
    )
    
    # 构建消息历史
    messages = []
    for chat in reversed(chat_history):
        messages.append({"role": chat.role, "content": chat.content})
    
    # 创建Agent配置
    agent = Agent(
        name=agent_db.name,
        instructions=agent_db.instructions or "你是一个有用的AI助手。",
        model="gpt-3.5-turbo",
    )
    
    # 创建流式响应
    async def generate():
        full_response = ""
        try:
            # 使用Runner.run_streamed进行流式处理
            result = Runner.run_streamed(
                agent,
                input=message,
                context={"messages": messages}
            )
            
            # 流式处理事件
            async for event in result.stream_events():
                # 处理原始响应事件（逐Token输出）
                if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                    content = event.data.delta
                    if content:
                        full_response += content
                        yield f"data: {json.dumps({'content': content})}\n\n"
            
            # 在后台任务中保存完整响应
            background_tasks.add_task(
                save_assistant_message,
                db=db,
                agent_id=agent_id,
                user_id=current_user.id,
                content=full_response,
            )
            
            yield f"data: {json.dumps({'content': '[DONE]'})}\n\n"
        except Exception as e:
            error_message = f"处理消息时出错: {str(e)}"
            yield f"data: {json.dumps({'error': error_message})}\n\n"
            
            # 在后台任务中保存错误消息
            background_tasks.add_task(
                save_assistant_message,
                db=db,
                agent_id=agent_id,
                user_id=current_user.id,
                content=error_message,
            )
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
    )


# 后台任务：保存助手消息
def save_assistant_message(db: Session, agent_id: int, user_id: int, content: str):
    """后台任务：保存助手消息到数据库"""
    crud.chat_message.create(
        db=db,
        obj_in=schemas.ChatMessageCreate(
            role="assistant",
            content=content,
            agent_id=agent_id,
            user_id=user_id,
        ),
    ) 