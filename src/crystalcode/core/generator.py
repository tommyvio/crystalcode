import logging
from typing import Optional
from transformers import pipeline
from crystalcode.constants import LANGUAGE_TEMPLATES
from crystalcode.config import Config

# Setting up logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(Config.LOG_FILE)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

class CodeGenerator:
    def __init__(self, model_name: str = Config.MODEL_NAME):
        self.generator = pipeline("text-generation", model=model_name)
        self.language_templates = LANGUAGE_TEMPLATES

    def generate_code(self, prompt: str, language: str = "python", code_type: str = "function", max_length: int = Config.MAX_LENGTH) -> Optional[str]:
        try:
            logger.info(f"Generating code for prompt: {prompt}, language: {language}, code type: {code_type}")
            template = self.language_templates.get(language, {}).get(code_type)
            if template:
                prompt = f"Using {language}, {prompt}\nFollow this template:\n{template}"

            generated = self.generator(prompt, max_length=max_length, num_return_sequences=1, temperature=Config.TEMPERATURE)
            code = generated[0]["generated_text"]
            return self._post_process_code(code, language)
        except Exception as e:
            logger.error(f"Code generation failed: {str(e)}")
            raise ValueError(f"Code generation failed: {str(e)}")

    def _post_process_code(self, code: str, language: str) -> str:
        if language == "python":
            try:
                ast.parse(code)
            except SyntaxError as e:
                logger.warning(f"Invalid Python code generated: {str(e)}")
                raise ValueError(f"Generated invalid Python code: {str(e)}")
        return code
