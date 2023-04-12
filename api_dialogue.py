import os
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from core.database import doc_create, doc_delete, doc_update, paginate_find
from core.dependencies import get_paginate_parameters
from core.dynamic import get_apis_configs
from apis.bases.models import UserGlobal, Paginate
from apis.bases.api_me import read_me_info
from .models import COL_DIALOGUE, DialogueBase, DialogueCreate, DialogueUpdate, DialogueRead
from .validate import DialogueObjIdParams, get_me_dialogue
from .utils import gpt_35_api

router = APIRouter(prefix='/dialogue', )


@router.post(
    '/free/',
    response_model=DialogueRead,
    summary='创建对话 (无权限)',
)
async def gpt_35_create_dialogue(create_data: DialogueCreate,
                                 user: UserGlobal = Depends(read_me_info)):
    create_json = jsonable_encoder(create_data)
    create_json['messages'] = [
        {
            'role': 'system',
            'content': create_json['system_role']
        },
    ]
    create_json['create_username'] = user.username
    doc_create(COL_DIALOGUE, create_json)
    return DialogueRead(**create_json)


@router.get(
    '/free/',
    response_model=Paginate,
    summary='读取对话 (分页|无权限)',
)
async def gpt_35_read_dialogue_page(
        paginate: dict = Depends(get_paginate_parameters),
        user: UserGlobal = Depends(read_me_info)):
    query_content = {'create_username': user.username}
    results = await paginate_find(
        collection=COL_DIALOGUE,
        paginate_parameters=paginate,
        query_content=query_content,
        item_model=DialogueRead,
    )
    return results


@router.delete(
    '/{dialogue_id}/free/',
    summary='删除对话 (无权限)',
)
async def gpt_35_delete_dialogue(dialogue_id: DialogueObjIdParams,
                                 user: UserGlobal = Depends(read_me_info)):
    dialogue_data = get_me_dialogue(dialogue_id, user)
    doc_delete(COL_DIALOGUE, dialogue_data)
    return {}


@router.put(
    '/{dialogue_id}/free/',
    summary='更新对话 (无权限)',
)
async def gpt_35_update_dialogue(dialogue_id: DialogueObjIdParams,
                                 update_data: DialogueBase,
                                 user: UserGlobal = Depends(read_me_info)):
    dialogue_data = get_me_dialogue(dialogue_id, user)
    update_json = update_data.dict(exclude_unset=True)
    doc_update(COL_DIALOGUE, {'_id': dialogue_id}, update_json)
    return {}


@router.put(
    '/{dialogue_id}/message/free/',
    summary='更新对话消息 (无权限)',
)
async def gpt_35_update_dialogue_message(
    dialogue_id: DialogueObjIdParams,
    update_data: DialogueUpdate,
    user: UserGlobal = Depends(read_me_info)):
    dialogue_data = get_me_dialogue(dialogue_id, user)
    update_json = update_data.dict(exclude_unset=True)
    messages = dialogue_data['messages']
    messages.append({'role': 'user', 'content': update_json['new_message']})
    module = os.path.basename(os.path.dirname(os.path.realpath(__file__)))
    configs = get_apis_configs(module)
    results, error_desc = gpt_35_api(configs.openai_api_key, messages)
    if not results:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_desc,
        )
    doc_update(COL_DIALOGUE, {'_id': dialogue_id}, {'messages': messages})
    return {'messages': messages[-2:]}


@router.get(
    '/{dialogue_id}/free/',
    response_model=DialogueRead,
    summary='读取对话 (无权限)',
)
async def gpt_35_read_dialogue(dialogue_id: DialogueObjIdParams,
                               user: UserGlobal = Depends(read_me_info)):
    dialogue_data = get_me_dialogue(dialogue_id, user)
    return DialogueRead(**dialogue_data)
