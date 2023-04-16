import os
import asyncio
from bson.objectid import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import StreamingResponse
from core.database import doc_create, doc_delete, doc_update, paginate_find
from core.dependencies import get_paginate_parameters
from core.dynamic import get_apis_configs
from apis.bases.models import UserGlobal, Paginate
from apis.bases.api_me import read_me_info
from .models import COL_DIALOGUE, DialogueBase, DialogueRead, DialogueMessageUpdate
from .validate import DialogueObjIdParams, get_me_dialogue
from .utils import gpt_35_api, gpt_35_api_stream

router = APIRouter(prefix='/dialogue', )


async def coroutine_task_summary_dialogue(dialogue_id: ObjectId, api_key: str,
                                          messages: list):
    """ 协程任务: 总结对话内容 """
    await asyncio.sleep(25)
    print(f'待总结内容 = {messages[1:]}')
    questions = [
        {
            'role': 'system',
            'content': '你是善于总结对话内容的标题作者'
        },
        {
            'role': 'user',
            'content': f'为以下对话取一个标题\n{messages[1:]}'
        },
    ]
    results, error_desc = gpt_35_api(api_key, questions)
    await asyncio.sleep(10)
    if not results:
        print(f'总结异常 = {error_desc}')
    else:
        print(f'总结后的 = {questions[-1:]}')
    await asyncio.sleep(25)
    return


@router.post(
    '/free/',
    response_model=DialogueRead,
    summary='创建对话 (无权限)',
)
async def gpt_35_create_dialogue(create_data: DialogueBase,
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
    messages = dialogue_data['messages']
    messages[0]['content'] = update_json['system_role']
    update_json['messages'] = messages
    doc_update(COL_DIALOGUE, {'_id': dialogue_id}, update_json)
    return {}


@router.put(
    '/{dialogue_id}/name/free/',
    summary='更新对话名称 (无权限)',
)
async def gpt_35_update_dialogue_name(
    dialogue_id: DialogueObjIdParams,
    user: UserGlobal = Depends(read_me_info)):
    dialogue_data = get_me_dialogue(dialogue_id, user)
    module = os.path.basename(os.path.dirname(os.path.realpath(__file__)))
    configs = get_apis_configs(module)
    asyncio.create_task(
        coroutine_task_summary_dialogue(dialogue_id, configs.openai_api_key,
                                        dialogue_data['messages']))
    return {}


@router.put(
    '/{dialogue_id}/message/free/',
    summary='更新对话消息 (无权限)',
)
async def gpt_35_update_dialogue_message(
    dialogue_id: DialogueObjIdParams,
    update_data: DialogueMessageUpdate,
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


@router.put(
    '/{dialogue_id}/message/stream/free/',
    summary='更新对话消息 (流|无权限)',
)
async def gpt_35_update_dialogue_message_stream(
    dialogue_id: DialogueObjIdParams,
    update_data: DialogueMessageUpdate,
    user: UserGlobal = Depends(read_me_info)):
    dialogue_data = get_me_dialogue(dialogue_id, user)
    update_json = update_data.dict(exclude_unset=True)
    messages = dialogue_data['messages']
    messages.append({'role': 'user', 'content': update_json['new_message']})
    module = os.path.basename(os.path.dirname(os.path.realpath(__file__)))
    configs = get_apis_configs(module)
    results, error_desc, response = gpt_35_api_stream(
        configs.openai_api_key,
        messages,
    )
    if not results:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_desc,
        )
    completion = {'role': '', 'content': ''}

    def data_streamer():
        for _data in response:
            if _data['choices'][0]['finish_reason'] == 'stop':
                messages.append(completion)
                doc_update(
                    COL_DIALOGUE,
                    {'_id': dialogue_id},
                    {'messages': messages},
                )
            for delta_k, delta_v in _data['choices'][0]['delta'].items():
                completion[delta_k] += delta_v
                if delta_k == 'content':
                    yield delta_v

    return StreamingResponse(data_streamer(), media_type='text/event-stream')


@router.get(
    '/{dialogue_id}/free/',
    response_model=DialogueRead,
    summary='读取对话 (无权限)',
)
async def gpt_35_read_dialogue(dialogue_id: DialogueObjIdParams,
                               user: UserGlobal = Depends(read_me_info)):
    dialogue_data = get_me_dialogue(dialogue_id, user)
    return DialogueRead(**dialogue_data)
