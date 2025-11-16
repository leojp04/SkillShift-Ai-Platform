# SkillShift.AI — Plataforma de Requalificação com IA

Plataforma de requalificação profissional baseada em Inteligência Artificial criada como parte da Global Solution da FIAP. A solução sugere macro-áreas de carreira e trilhas de cursos alinhadas ao perfil psicométrico dos participantes.

## Badges

![Status](https://img.shields.io/badge/Status-IA%20Ativa-success)
![API](https://img.shields.io/badge/API-Flask-blue)
![Modelos](https://img.shields.io/badge/Modelos-RandomForest%20%2B%20KMeans-orange)
![Python](https://img.shields.io/badge/Python-3.11-3776AB)

---

## Visão Geral da Arquitetura

A solução é composta por:

- **Modelo 1 — Classificação (RandomForestClassifier)**
  - Prevê **3 macro-áreas de carreira**: `Tech`, `Business`, `Human`.
  - Usa 10 features psicométricas e de aptidão.

- **Modelo 2 — Agrupamento (K-Means + StandardScaler)**
  - Agrupa perfis em **3 clusters** com base nas mesmas 10 features.
  - Cada cluster recebe uma **trilha de cursos recomendada**.

Ambos os modelos são treinados em Python, serializados em `.joblib` e carregados pela **API Flask** para respostas em tempo real.

---

## Diagrama da Arquitetura

```mermaid
flowchart LR
    User[Usuário / Plataforma] --> API[API Flask / SkillShift.AI]
    API --> Model1[RandomForest\nClassificação]
    API --> Model2[K-Means + Scaler\nAgrupamento]
    Model1 --> MacroArea[Macro-área]
    Model2 --> Recs[Recomendações]
```

## Arquivos dos modelos

```
api/models/
  modelo_career_area_3classes.joblib
  modelo_perfis_clusters.joblib
```

## Features utilizadas pelos modelos

```
O_score
C_score
E_score
A_score
N_score
Numerical Aptitude
Spatial Aptitude
Perceptual Aptitude
Abstract Reasoning
Verbal Reasoning
```

## Documentação da API

### A) GET /

{
  "mensagem": "SkillShift.AI API online"
}

### B) POST /predict-area

- Entrada: JSON contendo as 10 features.
- Saída:

  ```json
  {
    "macro_area": "Tech",
    "explicacao": "texto explicando a macro-área"
  }
  ```

### C) POST /cluster-profile

- Entrada: JSON contendo as 10 features.
- Saída:

  ```json
  {
    "cluster": 1,
    "cursos_recomendados": [...]
  }
  ```

## Exemplos de chamadas via CURL (CMD)

```bash
curl -X POST http://127.0.0.1:5000/predict-area -H "Content-Type: application/json" -d "{\"O_score\":6.5,\"C_score\":7.8,\"E_score\":5.9,\"A_score\":6.2,\"N_score\":4.1,\"Numerical Aptitude\":7.5,\"Spatial Aptitude\":6.8,\"Perceptual Aptitude\":7.2,\"Abstract Reasoning\":7.9,\"Verbal Reasoning\":6.3}"
```

```bash
curl -X POST http://127.0.0.1:5000/cluster-profile -H "Content-Type: application/json" -d "{\"O_score\":6.5,\"C_score\":7.8,\"E_score\":5.9,\"A_score\":6.2,\"N_score\":4.1,\"Numerical Aptitude\":7.5,\"Spatial Aptitude\":6.8,\"Perceptual Aptitude\":7.2,\"Abstract Reasoning\":7.9,\"Verbal Reasoning\":6.3}"
```

## Exemplo de uso em Python

```python
import requests

payload = { ... }

r = requests.post("http://127.0.0.1:5000/predict-area", json=payload)
print(r.json())
```

## Instalação e Execução da API

```
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python api/app.py
```

## Estrutura do Projeto

```
skillshift-ai-platform/
│
├── api/
│   └── app.py
├── notebooks/
│   ├── SkillShift_Ai_Platform.ipynb
│   └── skillshift_ai_platform.py
├── models/
│   ├── modelo_career_area_3classes.joblib
│   └── modelo_perfis_clusters.joblib
├── data/
│   └── Data_final.csv
├── requirements.txt
└── README.md
```

## Aviso sobre compatibilidade

Os modelos foram treinados com scikit-learn 1.6.1 e executados com 1.5.2, o que gera warnings esperados durante o carregamento.
