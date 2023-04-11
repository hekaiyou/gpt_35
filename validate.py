from fastapi import HTTPException, status
from core.database import doc_count, doc_read
from core.validate import ObjIdParams
from .models import COL_DIALOGUE


class DialogueObjIdParams(ObjIdParams):

    @classmethod
    def validate_doc(cls, oid):
        return doc_count(COL_DIALOGUE, {'_id': oid})


def get_me_dialogue(dialogue_id, user):
    dialogue = doc_read(COL_DIALOGUE, {'_id': dialogue_id})
    if user.username != dialogue['create_username']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='当前用户非创建用户',
        )
    return dialogue
