# SkillShift.AI — Plataforma de Requalificação com IA

Plataforma de requalificação profissional baseada em Inteligência Artificial criada como parte da Global Solution da FIAP. A solução sugere macro-áreas de carreira e trilhas de cursos alinhadas ao perfil psicométrico dos participantes.

## Badges

![Status](https://img.shields.io/badge/Status-IA%20Ativa-success)
![API](https://img.shields.io/badge/API-Flask-blue)
![Modelos](https://img.shields.io/badge/Modelos-RandomForest%20%2B%20KMeans-orange)
![Python](https://img.shields.io/badge/Python-3.11-3776AB)

## Visão Geral da Arquitetura

### • Modelo 1 — Classificação (RandomForestClassifier)

- Classes previstas: Tech, Business, Human.
- Consome 10 features psicométricas e cognitivas.

### • Modelo 2 — Agrupamento (K-Means + StandardScaler)

- Agrupamento em 3 clusters.
- Realiza recomendação automática de trilhas.

Ambos os modelos foram treinados em Python, serializados em arquivos `.joblib` e são carregados pela API Flask para respostas em tempo real.

## Diagrama da Arquitetura

```mermaid
flowchart LR
    User --> API
    API --> Model1[RandomForest<br>Classificação]
    API --> Model2[K-Means<br>Clusters]
    Model1 --> MacroArea
    Model2 --> Recomendacoes
```

## Arquivos dos modelos

```
/models/
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

### A) POST /predict-area

- Entrada: JSON contendo as 10 features.
- Saída:

  ```json
  {
    "macro_area": "Tech",
    "explicacao": "texto explicando a macro-área"
  }
  ```

### B) POST /cluster-profile

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


