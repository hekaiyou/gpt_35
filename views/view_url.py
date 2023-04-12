from fastapi.responses import HTMLResponse
from core.dependencies import get_view_request
from fastapi import APIRouter, Cookie, Depends
from apis.templating import templates
from apis.gpt_35.validate import DialogueObjIdParams

router = APIRouter(prefix='/gpt_35', )


@router.get('/dialogue/', response_class=HTMLResponse, include_in_schema=False)
async def page_gpt_35_dialogue(request: dict = Depends(get_view_request)):
    return templates.TemplateResponse('gpt_35/dialogue.html', {**request})


@router.get('/dialogue/create/',
            response_class=HTMLResponse,
            include_in_schema=False)
async def page_gpt_35_dialogue_create(
        request: dict = Depends(get_view_request)):
    return templates.TemplateResponse('gpt_35/dialogue-edit.html', {**request})


@router.get('/dialogue/update/{dialogue_id}/',
            response_class=HTMLResponse,
            include_in_schema=False)
async def page_gpt_35_dialogue_update(
    dialogue_id: DialogueObjIdParams,
    request: dict = Depends(get_view_request)):
    return templates.TemplateResponse('gpt_35/dialogue-edit.html', {
        'item_id': str(dialogue_id),
        **request
    })


@router.get('/dialogue/message/{dialogue_id}/',
            response_class=HTMLResponse,
            include_in_schema=False)
async def page_gpt_35_dialogue_message(
    dialogue_id: DialogueObjIdParams,
    request: dict = Depends(get_view_request)):
    return templates.TemplateResponse('gpt_35/dialogue_message.html', {
        'item_id': str(dialogue_id),
        **request
    })
