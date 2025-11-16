# SkillShift.AI — Plataforma de Requalificação com IA

Plataforma de requalificação profissional que aplica modelos de IA para interpretar perfis psicométricos, identificar macro-áreas de carreira e recomendar trilhas de aprendizado conforme o cluster comportamental.

## Arquitetura da IA

- **Modelo de Classificação**: `RandomForestClassifier` treinado para classificar perfis nas macro-áreas Tech, Business e Human.
- **Modelo de Agrupamento**: pipeline `StandardScaler` + `KMeans` (3 clusters) responsável por agrupar perfis e mapear trilhas recomendadas.
- Os dois modelos consomem exatamente o mesmo vetor de 10 features numéricas e são carregados a partir de artefatos `.joblib` localizados em `/api/models`.

## Modelo de Classificação (RandomForestClassifier — Tech, Business, Human)

- Entrada: vetor de 10 features psicométricas ordenadas conforme `FEATURE_COLS` do `api/app.py`.
- Saída: campo `macro_area` com o valor Tech, Business ou Human, acompanhado de `explicacao` textual embutida no código.
- Implementação: `modelo_area.predict(X)` é chamado no endpoint `/predict-area`; erros de validação retornam HTTP 400 e falhas de carregamento retornam HTTP 500.

## Modelo de Agrupamento (K-Means + StandardScaler — 3 clusters)

- Pré-processamento: `StandardScaler` serializado é aplicado para manter a mesma escala usada no treinamento.
- Agrupamento: `KMeans` com `n_clusters = 3` retorna o índice inteiro do cluster.
- Saída: `cluster` (0, 1 ou 2) e lista `cursos_recomendados` correspondente, definida estaticamente no `api/app.py`.

## Lista dos arquivos .joblib na pasta /models

- `/api/models/modelo_career_area_3classes.joblib` — RandomForestClassifier para macro-áreas.
- `/api/models/modelo_perfis_clusters.joblib` — Objeto contendo `scaler` e `kmeans` usados na etapa de clusterização.

## Lista completa das 10 features usadas pelos modelos

1. `O_score`
2. `C_score`
3. `E_score`
4. `A_score`
5. `N_score`
6. `Numerical Aptitude`
7. `Spatial Aptitude`
8. `Perceptual Aptitude`
9. `Abstract Reasoning`
10. `Verbal Reasoning`

## Explicação técnica dos dois endpoints da API Flask

- **POST `/predict-area`**: recebe JSON com as 10 features, chama `extrair_features`, executa `modelo_area.predict` e devolve `macro_area` + `explicacao`. Falta de campos ou dados não numéricos gera `400`; ausência do modelo gera `500`.
- **POST `/cluster-profile`**: consome o mesmo JSON, aplica `scaler_clusters.transform`, executa `kmeans.predict` e retorna `cluster` + `cursos_recomendados`. Erros de entrada retornam `400`; falta de artefatos produz `500`.

## Exemplos de requisições CURL (em uma linha, formato CMD)

```bash
curl -X POST http://127.0.0.1:5000/predict-area -H "Content-Type: application/json" -d "{\"O_score\":62.5,\"C_score\":71.2,\"E_score\":58.0,\"A_score\":69.1,\"N_score\":35.4,\"Numerical Aptitude\":78.0,\"Spatial Aptitude\":65.0,\"Perceptual Aptitude\":72.3,\"Abstract Reasoning\":74.8,\"Verbal Reasoning\":81.0}"
```
```json
{"macro_area":"Tech","explicacao":"Macro-área de tecnologia e engenharia: dados, programação, análise lógica, resolução de problemas complexos e trabalho com sistemas."}
```
```bash
curl -X POST http://127.0.0.1:5000/cluster-profile -H "Content-Type: application/json" -d "{\"O_score\":62.5,\"C_score\":71.2,\"E_score\":58.0,\"A_score\":69.1,\"N_score\":35.4,\"Numerical Aptitude\":78.0,\"Spatial Aptitude\":65.0,\"Perceptual Aptitude\":72.3,\"Abstract Reasoning\":74.8,\"Verbal Reasoning\":81.0}"
```
```json
{"cluster":0,"cursos_recomendados":["Trilha: Fundamentos de programação","Curso: Python para Iniciantes","Curso: Lógica de Programação"]}
```

## Guia de instalação e execução da API

1. **Criar venv**
   ```bash
   python -m venv .venv
   ```
2. **Ativar venv**
   - Linux/macOS: `source .venv/bin/activate`
   - Windows (CMD): `.\.venv\Scripts\activate`
3. **Instalar requirements**
   ```bash
   pip install -r requirements.txt
   ```
4. **Rodar `python api/app.py`**
   ```bash
   python api/app.py
   ```

## Aviso sobre a compatibilidade das versões do scikit-learn

Os modelos foram serializados com `scikit-learn==1.6.1`. Para evitar erros ao carregar os artefatos `.joblib`, mantenha a mesma versão especificada em `requirements.txt`; versões diferentes podem quebrar a desserialização ou alterar o comportamento dos algoritmos.

## Estrutura de diretórios esperada do projeto

```
skillshift-ai-platform/
├── README.md
├── requirements.txt
├── api/
│   ├── app.py
│   └── models/
│       ├── modelo_career_area_3classes.joblib
│       └── modelo_perfis_clusters.joblib
├── data/
│   └── ...
└── documentacao_modelos_ia.txt
```


