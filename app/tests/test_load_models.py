import pytest
import json
from .base_test_case import BaseTestCase
from app.settings import (CONFIG_JSON_PATH)
from app.helpers.config import Config


class TestLoadModels():

    def test_load_models_with_warnings(self):
        
        self.config_data = {
            "languages": {
                "es": "Spanish",
                "ca": "Catalan",
                "en": "English",
                "fr": "French",
                "de": "German",
                "it": "Italian",
                "pt": "Portuguese"
            },
            "models": [
                {
                "src": "ca",
                "tgt": "es",
                "model_type": "ctranslator2",
                "hugging_face_repo_id": "projecte-aina/aina-translator-ca-es",
                "model_path": "aina-translator-ca-es",
                "src_sentencepiece_model": "spm.model",
                "tgt_sentencepiece_model": "spm.model",
                "sentence_split": "nltk",
                "pipeline": {
                    "sentencepiece": True,
                    "translate": True
                }
            }]
        }

        self.config = Config(config_data=self.config_data, models_to_load=["all"])
        # languages
        assert self.config.language_codes == {
                "es": "Spanish",
                "ca": "Catalan",
                "en": "English",
                "fr": "French",
                "de": "German",
                "it": "Italian",
                "pt": "Portuguese"
         }
    
        assert self.config.languages_list == {'ca': {'es': ['ca-es']}}

        # models
        assert len(self.config.loaded_models) == 1

        assert 'ca-es' in self.config.loaded_models
        model = self.config.loaded_models['ca-es']
        assert model['src'] == 'ca'
        assert model['tgt'] == 'es'

        # pipeline
        assert model['sentence_segmenter'].__name__ == 'nltk_sentence_segmenter'
        assert len(model['preprocessors']) == 1
        assert len(model['postprocessors']) == 1
        assert 'get_sentencepiece_segmenter' in str(model['preprocessors'])
        assert 'get_sentencepiece_desegmenter' in str(model['postprocessors'])
        assert 'get_batch_ctranslator' in str(model['translator'])
