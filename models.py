from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from core.validate import ObjId
from core.dynamic import set_username_binding

COL_DIALOGUE = 'gpt_35_dialogue'

set_username_binding(COL_DIALOGUE, ['create_username'])


class DialogueBase(BaseModel):
    """ 对话的基础模型
    id: ObjId = Field(alias='_id', title='对话ID')
    dialogue_name: Optional[str] = Field(title='对话名称', default='新对话')
    system_role: Optional[str] = Field(title='系统角色的人设', default='你是一个乐于助人的助手。')
    messages: List[Dict] = Field(
        title='完整对话',
        default=[
            {
                'role': 'system',
                'content': '你是一个乐于助人的助手。'
            },
        ],
    )
    create_username: str = Field(title='创建用户名称', )
    auto_naming: bool = Field(title='是否自动命名', )
    create_time: datetime = datetime.utcnow()
    update_time: datetime = datetime.utcnow()
    """
    dialogue_name: Optional[str] = Field(title='对话名称', default='新对话')
    system_role: Optional[str] = Field(title='系统角色的人设', default='你是一个乐于助人的助手。')


class DialogueMessageUpdate(BaseModel):
    """ 对话消息的更新模型 """
    new_message: Optional[str] = Field(title='新消息', )


class DialogueRead(DialogueBase):
    """ 对话的读取模型 """
    id: ObjId = Field(alias='_id', title='对话ID')
    messages: List[Dict] = Field(
        title='完整对话',
        default=[
            {
                'role': 'system',
                'content': '你是一个乐于助人的助手。'
            },
        ],
    )
    create_username: str = Field(title='创建用户名称', )
    auto_naming: bool = Field(title='是否自动命名', )
    create_time: datetime = datetime.utcnow()
    update_time: datetime = datetime.utcnow()
