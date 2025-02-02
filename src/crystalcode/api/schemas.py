from pydantic import BaseModel

class GenerateCodeRequest(BaseModel):
    prompt: str
    language: str = "python"
    code_type: str = "function"

class AnalyzeCodeRequest(BaseModel):
    code: str
    language: str = "python"

class OptimizeCodeRequest(BaseModel):
    code: str
    language: str = "python"
