---
title: Movie Recommender
emoji: 🎬
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 5.25.0
app_file: app.py
pinned: false
---

# 🎬 Movie Recommender System

Content-based фильтр рекомендаций фильмов. Вводишь название - получаешь 10 похожих.

## 🚀 Демо
Попробуй онлайн: [Hugging Face Space](https://huggingface.co/spaces/Polva31/movie-recommender)

## 📊 Как это работает
- Использует данные TMDB 5000 (4803 фильма)
- Анализирует жанры, актеров, режиссера, ключевые слова
- Считает косинусную схожесть между фильмами

## 🛠 Технологии
- Python
- Pandas, NumPy
- Scikit-learn
- Gradio

## 🎯 Примеры
- Avatar → научная фантастика, космос
- The Dark Knight → похожие боевики
- Toy Story → анимация, приключения
