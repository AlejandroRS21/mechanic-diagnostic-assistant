import requests
import json
from typing import List, Dict, Optional
from src.utils.helpers import get_logger
from src.utils.config import OPENROUTER_MODEL

logger = get_logger(__name__)

DEFAULT_API_URL = "https://openrouter.ai/api/v1/models"

class ModelManager:
    def __init__(self):
        self.available_models: List[Dict] = []
        self.failed_models: set = set()
        self.current_model_index: int = 0
        self._refresh_models()

    def _refresh_models(self):
        """Fetch free models from OpenRouter."""
        logger.info("Fetching free models from OpenRouter...")
        self.available_models = []
        
        # Add configured model first if specified (and not default placeholder)
        if OPENROUTER_MODEL and OPENROUTER_MODEL != "openai/gpt-4":
            logger.info(f"Adding configured model: {OPENROUTER_MODEL}")
            self.available_models.append({
                "id": OPENROUTER_MODEL,
                "name": f"{OPENROUTER_MODEL} (Configured)"
            })
            
        self.available_models.extend(self.get_free_models())
        
        # Fallback if no models found
        if not self.available_models:
            logger.warning("No free models found on OpenRouter! Using fallback list.")
            self.available_models = [
                {"id": "mistralai/mistral-7b-instruct:free", "name": "Mistral 7B (Free)"},
                {"id": "meta-llama/llama-3.1-8b-instruct:free", "name": "Llama 3.1 8B (Free)"},
                {"id": "google/gemma-2-9b-it:free", "name": "Gemma 2 9B (Free)"},
                {"id": "microsoft/phi-3-mini-128k-instruct:free", "name": "Phi-3 Mini (Free)"},
                {"id": "qwen/qwen-2-7b-instruct:free", "name": "Qwen 2 7B (Free)"}
            ]
            
        self.failed_models.clear()
        self.current_model_index = 0
        logger.info(f"Total available models: {len(self.available_models)}")

    def get_current_model_id(self) -> Optional[str]:
        """Get the ID of the current active model."""
        if not self.available_models:
            self._refresh_models()
        
        while self.current_model_index < len(self.available_models):
            model = self.available_models[self.current_model_index]
            model_id = model.get("id")
            if model_id not in self.failed_models:
                return model_id
            self.current_model_index += 1
        
        # If we ran out of models, try refreshing once
        if self.failed_models:
            logger.info("Ran out of models, refreshing list...")
            self._refresh_models()
            if self.available_models:
                return self.available_models[0].get("id")
        
        return None

    def mark_current_failed(self):
        """Mark the current model as failed and advance to next."""
        if self.current_model_index < len(self.available_models):
            model_id = self.available_models[self.current_model_index].get("id")
            logger.warning(f"Marking model {model_id} as failed.")
            self.failed_models.add(model_id)
            self.current_model_index += 1

    def get_current_model_name(self) -> str:
        """Get human readable name of current model."""
        if self.current_model_index < len(self.available_models):
            return self.available_models[self.current_model_index].get("name", "Unknown")
        return "None"

    @staticmethod
    def get_all_models(api_url: str = DEFAULT_API_URL, timeout: int = 30):
        """Obtiene todos los modelos disponibles desde OpenRouter (JSON completo)."""
        try:
            response = requests.get(api_url, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            logger.error("Error: Timeout al conectar con OpenRouter")
            return {}
        except requests.exceptions.RequestException as e:
            logger.error(f"Error de conexión: {e}")
            return {}

    @staticmethod
    def _normalize_price_value(value):
        """Intenta convertir el value en float, devuelve None si no es numérico."""
        if value is None:
            return None
        if isinstance(value, (int, float)):
            return float(value)
        try:
            return float(str(value).strip())
        except Exception:
            return None

    @staticmethod
    def is_pricing_free(pricing) -> bool:
        """Determina si el pricing indica un modelo gratuito."""
        if not pricing or not isinstance(pricing, dict):
            return False

        price_keys = [
            "prompt", "completion", "price", "unit_price",
            "prompt_price", "completion_price", "value", "amount"
        ]

        numeric_values = []
        for key in price_keys:
            v = ModelManager._normalize_price_value(pricing.get(key))
            if v is not None:
                numeric_values.append(v)

        if not numeric_values:
            return False

        return all(v == 0.0 for v in numeric_values)

    @classmethod
    def get_free_models(cls, api_url: str = DEFAULT_API_URL, timeout: int = 30):
        """Devuelve lista de modelos (dicts) que son gratuitos según 'pricing'."""
        data = cls.get_all_models(api_url=api_url, timeout=timeout)
        models = []

        if isinstance(data, dict) and "data" in data:
            models = data.get("data", [])
        elif isinstance(data, list):
            models = data
        else:
            return []

        free_models = []
        for model in models:
            if cls.is_pricing_free(model.get("pricing")):
                free_models.append(model)
        
        # Sort by preference: Prioritize Mistral models
        def sort_key(model):
            name = model.get("name", "").lower()
            if "mistral" in name:
                return 0  # Highest priority
            if "llama" in name:
                return 1
            return 2
            
        free_models.sort(key=sort_key)
        
        return free_models
