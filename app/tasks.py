from celery import shared_task

from app.helpers.config import Config
from app.utils.translate import translate_text


@shared_task
def translate_text_async(model_id, text, src, tgt):
    config = Config(model_id=model_id, log_messages=False)
    translate = translate_text(model_id, text, src, tgt)
    return translate


@shared_task
def translate_batch_async(model_id, texts):
    config = Config(model_id=model_id, log_messages=False)

    translated_batch = []
    for sentence in texts:
        translation = translate_text(model_id, sentence)
        translated_batch.append(translation)

    return translated_batch


@shared_task
def add(x, y):
    return x + y