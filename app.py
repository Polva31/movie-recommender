import pickle
import pandas as pd
import gradio as gr
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

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

    return df_clean['original_title'].iloc[movie_indices].tolist()


def recommend_movies(title):
    recs = get_recommendations(title)
    return "\n".join(recs)


iface = gr.Interface(
    fn=recommend_movies,
    inputs=gr.Textbox(label="Введите название фильма"),
    outputs=gr.Textbox(label="Рекомендации"),
    title="🎬 Movie Recommender System",
    description="Введите любимый фильм и получите 10 похожих!",
    examples=[["Avatar"], ["The Dark Knight"], ["Inception"], ["Toy Story"]]
)

iface.launch()