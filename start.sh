#!/usr/bin/env bash
# Script de inicialização para o Render

# entra na pasta da API
cd api

# sobe o Gunicorn apontando para o objeto "app" dentro de app.py
gunicorn -w 1 -b 0.0.0.0:$PORT app:app
