from flask import Flask, request, jsonify
import joblib
import numpy as np
from pathlib import Path

app = Flask(__name__)

# ==========================================================
# Caminhos base
# ==========================================================

# pasta onde está o app.py (pasta api/)
BASE_DIR = Path(__file__).resolve().parent

# pasta models DENTRO da pasta api
MODEL_DIR = BASE_DIR / "models"

# Colunas usadas pelos modelos
FEATURE_COLS = [
    "O_score", "C_score", "E_score", "A_score", "N_score",
    "Numerical Aptitude", "Spatial Aptitude", "Perceptual Aptitude",
    "Abstract Reasoning", "Verbal Reasoning",
]

# ==========================================================
# Carregando modelos treinados (.joblib)
# ==========================================================

try:
    modelo_area = joblib.load(MODEL_DIR / "modelo_career_area_3classes.joblib")
    objeto_clusters = joblib.load(MODEL_DIR / "modelo_perfis_clusters.joblib")
    scaler_clusters = objeto_clusters["scaler"]
    kmeans = objeto_clusters["kmeans"]
    print("✅ Modelos carregados com sucesso.")
except Exception as e:
    print("❌ Erro ao carregar modelos:", e)
    modelo_area = None
    scaler_clusters = None
    kmeans = None


def extrair_features(json_data: dict) -> np.ndarray:
    """
    Lê o JSON da requisição e monta o vetor de features na ordem correta.
    """
    try:
        valores = [float(json_data[col]) for col in FEATURE_COLS]
    except KeyError as e:
        campo = str(e).strip("'")
        raise ValueError(f"Campo obrigatório ausente: {campo}")
    except ValueError as e:
        raise ValueError(f"Todos os campos devem ser numéricos. Detalhe: {e}")

    return np.array(valores).reshape(1, -1)


# ==========================================================
# Rota de saúde
# ==========================================================

@app.route("/")
def home():
    return jsonify({"mensagem": "SkillShift.AI API online"})


# ==========================================================
# MODELO 1 – Classificação em 3 macro-áreas
# ==========================================================

@app.route("/predict-area", methods=["POST"])
def predict_area():
    if modelo_area is None:
        return jsonify({"erro": "Modelo de classificação não foi carregado no servidor."}), 500

    try:
        data = request.get_json(force=True)
        X = extrair_features(data)
        pred = modelo_area.predict(X)[0]
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400

    explicacoes = {
        "Human": (
            "Macro-área voltada para perfis que gostam de trabalhar com pessoas: "
            "educação, saúde, psicologia, serviços sociais, liderança de times, etc."
        ),
        "Tech": (
            "Macro-área de tecnologia e engenharia: dados, programação, análise lógica, "
            "resolução de problemas complexos e trabalho com sistemas."
        ),
        "Business": (
            "Macro-área orientada a negócios: gestão, finanças, marketing, vendas, "
            "estratégia e tomada de decisão voltada a resultados."
        ),
    }

    return jsonify(
        {
            "macro_area": pred,
            "explicacao": explicacoes.get(pred, ""),
        }
    )


# ==========================================================
# MODELO 2 – Cluster de perfil (K-Means)
# ==========================================================

@app.route("/cluster-profile", methods=["POST"])
def cluster_profile():
    if scaler_clusters is None or kmeans is None:
        return jsonify({"erro": "Modelo de clusters não foi carregado no servidor."}), 500

    try:
        data = request.get_json(force=True)
        X = extrair_features(data)
        X_scaled = scaler_clusters.transform(X)
        cluster = int(kmeans.predict(X_scaled)[0])
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400

    recomendacoes = {
        0: [
            "Trilha: Fundamentos de programação",
            "Curso: Python para Iniciantes",
            "Curso: Lógica de Programação",
        ],
        1: [
            "Trilha: Design & Experiência do Usuário",
            "Curso: UX Design Essencial",
            "Curso: Prototipação no Figma",
        ],
        2: [
            "Trilha: Dados e Negócios",
            "Curso: Introdução a Análise de Dados",
            "Curso: Fundamentos de Power BI",
        ],
    }

    return jsonify(
        {
            "cluster": cluster,
            "cursos_recomendados": recomendacoes.get(cluster, []),
        }
    )


if __name__ == "__main__":
    app.run(debug=True)
