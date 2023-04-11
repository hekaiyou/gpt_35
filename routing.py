from fastapi import APIRouter
from . import api_dialogue

router = APIRouter(
    prefix='/gpt_35',
    tags=['gpt_35'],
)

router.include_router(api_dialogue.router)