import logging
from typing import List, Dict
from dataclasses import dataclass
import ast
from pylint import lint
from pylint.reporters import JSONReporter
import tempfile

# Setting up logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(Config.LOG_FILE)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

@dataclass
class CodeAnalysisResult:
    issues: List[Dict]
    metrics: Dict
    suggestions: List[str]

class CodeAnalyzer:
    def analyze_code(self, code: str, language: str = "python") -> CodeAnalysisResult:
        if language == "python":
            return self._analyze_python(code)
        else:
            raise ValueError(f"Unsupported language: {language}")

    def _analyze_python(self, code: str) -> CodeAnalysisResult:
        try:
            logger.info("Analyzing Python code...")
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py') as tmp:
                tmp.write(code)
                tmp.flush()

                reporter = JSONReporter()
                lint.Run([tmp.name], reporter=reporter, do_exit=False)

                tree = ast.parse(code)
                complexity = self._analyze_complexity(tree)
                patterns = self._detect_patterns(tree)

                return CodeAnalysisResult(
                    issues=reporter.messages,
                    metrics={"complexity": complexity},
                    suggestions=patterns
                )
        except Exception as e:
            logger.error(f"Code analysis failed: {str(e)}")
            raise ValueError(f"Code analysis failed: {str(e)}")

    def _analyze_complexity(self, tree: ast.AST) -> int:
        complexity = 0
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.Match)):
                complexity += 1
        return complexity

    def _detect_patterns(self, tree: ast.AST) -> List[str]:
        suggestions = []
        for node in ast.walk(tree):
            if isinstance(node, ast.For):
                suggestions.append("Consider using list comprehension instead of for loop")
        return suggestions
