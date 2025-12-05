"""
Language detection utility for the Mechanic Diagnostic Assistant.
Detects user input language and ensures responses are in the same language.
"""

from typing import Optional
import re

# Language patterns for detection
LANGUAGE_PATTERNS = {
    "es": {
        "name": "Spanish",
        "patterns": [
            r"\b(hola|hallo|el|la|que|como|donde|cuando|cual|quien|por|para|con|sin)\b",
            r"[áéíóúüñ]",  # Spanish-specific characters
            r"\b(tengo|hace|tiene|estoy|puedo|quiero|necesito|podrias|thanks)\b",
        ]
    },
    "en": {
        "name": "English",
        "patterns": [
            r"\b(hello|hi|the|a|an|what|how|where|when|why|who|is|are|have|has)\b",
            r"\b(i|you|he|she|it|we|they|do|does|can|could|would|should)\b",
        ]
    },
    "pt": {
        "name": "Portuguese",
        "patterns": [
            r"\b(ola|olá|o|a|que|como|onde|quando|qual|quem|por|para|com|sem)\b",
            r"[ãõé]",  # Portuguese-specific characters
            r"\b(tenho|faço|faz|estou|posso|quero|preciso|podia|obrigado)\b",
        ]
    },
    "fr": {
        "name": "French",
        "patterns": [
            r"\b(bonjour|salut|le|la|les|un|une|des|que|comment|où|quand|quel|qui)\b",
            r"[àâäæçéèêëïîôöœùûüœ]",  # French-specific characters
            r"\b(je|tu|il|elle|nous|vous|ils|elles|avoir|être)\b",
        ]
    },
}

class LanguageDetector:
    """Detect language from user input text."""
    
    @staticmethod
    def detect_language(text: str) -> str:
        """
        Detect the language of the input text.
        
        Args:
            text: User input text
            
        Returns:
            Language code (es, en, pt, fr) or 'en' as default
        """
        if not text or len(text.strip()) < 3:
            return "en"
        
        text_lower = text.lower()
        scores = {}
        
        for lang_code, lang_info in LANGUAGE_PATTERNS.items():
            score = 0
            for pattern in lang_info["patterns"]:
                matches = len(re.findall(pattern, text_lower, re.IGNORECASE))
                score += matches
            scores[lang_code] = score
        
        # Return language with highest score, default to English
        detected = max(scores.items(), key=lambda x: x[1])[0] if scores else "en"
        return detected if scores[detected] > 0 else "en"
    
    @staticmethod
    def get_language_name(lang_code: str) -> str:
        """Get human-readable language name."""
        return LANGUAGE_PATTERNS.get(lang_code, {}).get("name", "English")


class LanguageInstructions:
    """Get language-specific instructions for the agent."""
    
    INSTRUCTIONS = {
        "es": """Importante: El usuario escribió en español, así que DEBES responder completamente en español.
- Usa términos técnicos automotrices en español
- Sé profesional pero amigable
- Estructura tu respuesta con claridad""",
        
        "en": """Important: The user wrote in English, so you MUST respond completely in English.
- Use technical automotive terms in English
- Be professional but friendly
- Structure your response with clarity""",
        
        "pt": """Importante: O usuário escreveu em português, então você DEVE responder completamente em português.
- Use termos técnicos automotivos em português
- Seja profissional mas amigável
- Estruture sua resposta com clareza""",
        
        "fr": """Important: L'utilisateur a écrit en français, donc vous DEVEZ répondre complètement en français.
- Utilisez des termes techniques automobiles en français
- Soyez professionnel mais amical
- Structurez votre réponse avec clarté""",
    }
    
    @staticmethod
    def get_language_instruction(lang_code: str) -> str:
        """Get language-specific instruction for the LLM."""
        return LanguageInstructions.INSTRUCTIONS.get(lang_code, LanguageInstructions.INSTRUCTIONS["en"])


if __name__ == "__main__":
    # Test language detection
    test_texts = [
        "¿Tengo un código P0420, qué significa?",
        "Hello, what does the P0420 code mean?",
        "Olá, o que significa o código P0420?",
        "Bonjour, que signifie le code P0420?",
    ]
    
    detector = LanguageDetector()
    for text in test_texts:
        lang = detector.detect_language(text)
        print(f"Text: {text[:50]}...")
        print(f"Detected: {LanguageDetector.get_language_name(lang)} ({lang})\n")
