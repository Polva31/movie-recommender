import os
import pickle
import pandas as pd
import gradio as gr
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

if not os.path.exists('movie_data.pkl') or not os.path.exists('cosine_sim.pkl'):
    import setup

cosine_sim = pickle.load(open('cosine_sim.pkl', 'rb'))
df_clean = pd.read_pickle('movie_data.pkl')
indices = pd.Series(df_clean.index, index=df_clean['original_title']).drop_duplicates()

def get_recommendations(title):
    if title not in indices:
        return ["Фильм не найден. Попробуйте другое название."]
    
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    
    recommendations = df_clean['original_title'].iloc[movie_indices].tolist()
    return recommendations

def recommend_movies(title):
    if not title or title.strip() == "":
        return "⚠️ Пожалуйста, введите название фильма"
    
    recs = get_recommendations(title.strip())
    
    if isinstance(recs, list) and len(recs) > 0:
        if recs[0] == "Фильм не найден. Попробуйте другое название.":
            return f"❌ {recs[0]}"
        else:
            result = "## 🎯 Рекомендованные фильмы:\n\n"
            for i, movie in enumerate(recs, 1):
                result += f"{i}. 🎬 **{movie}**\n"
            return result
    return "❌ Ошибка при получении рекомендаций"

with gr.Blocks(title="Movie Recommender", theme=gr.themes.Soft()) as app:
    gr.Markdown("# 🎬 Рекомендатор фильмов")
    gr.Markdown("Введите название любимого фильма и получите 10 похожих рекомендаций!")
    
    with gr.Row():
        with gr.Column():
            input_text = gr.Textbox(
                label="Название фильма",
                placeholder="Например: Avatar, The Dark Knight, Inception...",
                lines=2
            )
            submit_btn = gr.Button("🔍 Найти похожие фильмы", variant="primary")
    
    with gr.Row():
        output_text = gr.Markdown("✨ Введите название фильма и нажмите кнопку")
    
    gr.Examples(
        examples=[
            ["Avatar"], 
            ["The Dark Knight"], 
            ["Inception"], 
            ["Toy Story"],
            ["Pulp Fiction"],
            ["The Matrix"]
        ],
        inputs=input_text,
        outputs=output_text,
        fn=recommend_movies,
        cache_examples=False
    )
    
    submit_btn.click(
        fn=recommend_movies,
        inputs=input_text,
        outputs=output_text
    )
    
    input_text.submit(
        fn=recommend_movies,
        inputs=input_text,
        outputs=output_text
    )
    
    gr.Markdown("---")
    gr.Markdown("⚡ Работает на основе косинусной схожести • Данные: TMDB 5000")

if __name__ == "__main__":
    app.launch(ssr=False)


