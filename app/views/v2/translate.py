from typing import Dict
import logging
from fastapi import APIRouter, HTTPException, status
from celery.result import AsyncResult

from app.helpers.config import Config
from app.utils.utils import get_model_id
from app.models.v1.translate import (
    BatchTranslationRequest,
    BatchTranslationResponse,
    LanguagesResponse,
    TranslationRequest,
    TranslationResponse,
)
from app.utils.translate import translate_text
from app.tasks import translate_text_async, translate_batch_async, add
from app.constants import MULTIMODALCODE

translate_v2 = APIRouter(prefix='/api/v2/translate')
DEVDEBUG = True
logger = logging.getLogger('console_logger')
def fetch_model_data_from_request(request):
    config = Config()

    src = config.map_lang_to_closest(request.src)
    tgt = config.map_lang_to_closest(request.tgt)
    use_multi = True if request.use_multi == 'True' else False

    #Get regular model_id
    model_id = get_model_id(
        src=src,
        tgt=tgt,
        alt_id=request.alt
    )

    compatible_model_ids = config._lookup_pair_in_languages_list(src, tgt, request.alt)

    if not compatible_model_ids:
        raise HTTPException(
                status_code=406,
                detail=f'Language pair {model_id} is not supported.',
            )

    if DEVDEBUG: 
        logger.debug(f'compatible_model_ids {compatible_model_ids}')
        if use_multi:
            logger.debug(f'use_multi {use_multi}')
    
    regular_model_exists = model_id in config.loaded_models
    multilingual_model_exists_for_pair = any([mid.startswith(MULTIMODALCODE) for mid in compatible_model_ids])

    if not regular_model_exists and not use_multi and multilingual_model_exists_for_pair:
        use_multi = True

    if use_multi:
        if multilingual_model_exists_for_pair:
            #fetch multimodal 
            # model_id = get_model_id(src=MULTIMODALCODE,
                                    # tgt=MULTIMODALCODE,
                                    # alt_id=request.alt)
            model_id = config._pair_to_model_id(compatible_model_ids[0])
            if len(compatible_model_ids) > 1:
                logger.warning(f"More than one compatible model. Choosing {compatible_model_ids[0]} among {compatible_model_ids}")

        else:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No multilingual model support for pair {src}-{tgt}. Remove flag `use_multi` from request',
        )

    if DEVDEBUG: logger.debug(f'model_id {model_id}')

    return model_id, src, tgt

@translate_v2.post('', status_code=status.HTTP_200_OK)
@translate_v2.post('/', status_code=status.HTTP_200_OK)
async def translate_sentence_async(request: TranslationRequest):
    model_id, src, tgt = fetch_model_data_from_request(request)

    # return TranslationResponse(translation=translation)
    print("Ankush============================================")
    task = translate_text_async.delay(model_id, request.text, src, tgt)
    print("Ankush============================================")

    return {'uid': task.id, 'status': task.status}

@translate_v2.post('/batch', status_code=status.HTTP_200_OK)
async def translate_batch(
    request: BatchTranslationRequest,
):
    model_id = get_model_id(request.src, request.tgt)
    task = translate_batch_async.delay(model_id, request.texts)
    return {'uid': task.id, 'status': task.status}


@translate_v2.get('', status_code=status.HTTP_200_OK)
@translate_v2.get('/', status_code=status.HTTP_200_OK)
async def languages() -> Dict:
    config = Config()
    return {'models': config.get_all_potential_languages()}


@translate_v2.get('/{uid}', status_code=status.HTTP_200_OK)
async def translate_sentence_async_result(uid):
    result = AsyncResult(uid)
    if result.successful():
        return TranslationResponse(translation=result.result)
    return {'status': result.status, 'info': result.info}


@translate_v2.get('/batch/{uid}', status_code=status.HTTP_200_OK)
async def translate_batch_async_result(uid):
    result = AsyncResult(uid)
    if result.successful():
        return BatchTranslationResponse(translation=result.result)
    return {'status': result.status, 'info': result.info}
