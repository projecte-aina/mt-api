"""
import json
import pytest
from app.utils.translate import translate_text
from app.utils.utils import get_model_id
from .base_test_case import BaseTestCase
from app.settings import (CONFIG_JSON_PATH)
from app.helpers.config import Config


class TestTranslations(BaseTestCase):

    @pytest.fixture(autouse=True)
    def setup_before_each_test(self):
        with open(CONFIG_JSON_PATH, 'r') as jsonfile:
            self.config_data = json.load(jsonfile)
        self.config = Config(config_data=self.config_data, models_to_load=["es-ca", "ca-es"])

    def test_translate_text_es_ca(self):
        model_id = get_model_id('es', 'ca')
        text = 'Hola, ¿Cómo estás?'
        expected_translation = 'Hola, com estàs?'
        translation = translate_text(model_id, text, 'es', 'ca')
        assert translation == expected_translation


        
    def test_translate_text_ca_es(self):
        model_id = get_model_id('ca', 'es')
        text = 'Hola, com estàs?'
        expected_translation = 'Hola, ¿cómo estás?'
        translation = translate_text(model_id, text, 'ca', 'es')
        assert translation == expected_translation
"""
