from flask import Flask, request, jsonify
from crystalcode.core.generator import CodeGenerator
from crystalcode.core.analyzer import CodeAnalyzer
from crystalcode.core.optimizer import CodeOptimizer
from crystalcode.api.schemas import GenerateCodeRequest, AnalyzeCodeRequest, OptimizeCodeRequest

# Initialize the Flask application
app = Flask(__name__)
generator = CodeGenerator()
analyzer = CodeAnalyzer()
optimizer = CodeOptimizer()

@app.route("/generate", methods=["POST"])
def generate():
    data = GenerateCodeRequest(**request.json)
    try:
        code = generator.generate_code(data.prompt, data.language, data.code_type)
        return jsonify({"code": code})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/analyze", methods=["POST"])
def analyze():
    data = AnalyzeCodeRequest(**request.json)
    try:
        results = analyzer.analyze_code(data.code, data.language)
        return jsonify({
            "issues": results.issues,
            "metrics": results.metrics,
            "suggestions": results.suggestions
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/optimize", methods=["POST"])
def optimize():
    data = OptimizeCodeRequest(**request.json)
    try:
        optimizations = optimizer.optimize_code(data.code, data.language)
        return jsonify({"optimizations": optimizations})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=Config.DEBUG_MODE, port=Config.API_PORT)
