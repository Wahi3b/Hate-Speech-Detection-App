from flask import current_app
from app import db
from lime.lime_text import LimeTextExplainer
import torch
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
import networkx as nx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from app.models import Explainable,Tweets
from app import db
import os
from sqlalchemy import func

tokenizer = AutoTokenizer.from_pretrained('./roBERTa-model')
model = AutoModelForSequenceClassification.from_pretrained('./roBERTa-model')


def generate_lime_explanation(text, tweet_id):
    explainer = LimeTextExplainer(class_names=["Neutral", "Hateful"])
    explanation = explainer.explain_instance(
        text,
        classifier_fn=predict_proba,
        num_features=10,
        num_samples=500
    )

    hateful_index = explanation.class_names.index("Hateful")
    local_exp_hateful = dict(explanation.local_exp[hateful_index])

    
    words_to_add = []
    for i, weight in local_exp_hateful.items():
        if weight > 0:
            word = explanation.domain_mapper.indexed_string.word(i)
            add_word = Explainable(tweet_id=tweet_id, tweet_word=word, word_probability=weight)
            words_to_add.append(add_word)

   
    db.session.add_all(words_to_add)
    try:
        db.session.commit()
    except Exception as e:
        print(f"Failed to commit: {e}")
        db.session.rollback()

def predict_proba(texts):
    
    inputs = tokenizer(texts, return_tensors="pt", padding=True, truncation=True, max_length=128).to(model.device)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.logits.softmax(dim=-1).cpu().numpy()

def graph(acc_id):
    G = nx.Graph()
    tweets = Tweets.query.filter_by(account_handler=acc_id, tweet_sentiment=1).all()
    if tweets:
        for tweet in tweets:
            words = Explainable.query.filter_by(tweet_id=tweet.tweet_id).all()
            for word in words:
                if G.has_node(word.tweet_word):
                    current_prob = G.nodes[word.tweet_word].get('prob', 0) 
                    if word.word_probability > current_prob:
                        G.nodes[word.tweet_word]['prob'] = word.word_probability
                else:
                    G.add_node(word.tweet_word, prob=word.word_probability)
            word_list = [word.tweet_word for word in words]
            for i in range(len(word_list)):
                for j in range(i + 1, len(word_list)):
                    G.add_edge(word_list[i], word_list[j])
        # degrees = dict(G.degree())
        # top_nodes = sorted(degrees, key=degrees.get, reverse=True)[:20]
        # subG = G.subgraph(top_nodes)
        min_size = 1000  
        max_size = 5000  
        node_sizes = [(G.nodes[node]['prob'] * (max_size - min_size)) + min_size for node in G]

        
        degrees = dict(G.degree())
        # max_degree = max(degrees[node] for node in subG.nodes()) 
        max_degree = max(degrees.values())  # Find the highest degree
        colors = ['#dc3545' if degrees[node] == max_degree  else '#007bff' for node in G.nodes()]

        pos = nx.spring_layout(G, k=1.1, scale=1)  # Adjust 'k' for more spread

        plt.figure(figsize=(12, 12), dpi=300)
        # nx.draw(subG, pos, with_labels=True, node_size=node_sizes, node_color=colors, font_size=16, font_color='black')
        nx.draw(G, pos, with_labels=True, node_size=node_sizes, node_color=colors, font_size=16, font_color='black')

        plt.title('Network of hateful words that this account has used')
        directory_path = os.path.join(current_app.root_path, 'static', 'graphs')
        image_filename = f"{acc_id}_graph.jpg"
        full_image_path = os.path.join(directory_path, image_filename)
        plt.savefig(full_image_path)
        plt.close()
        return image_filename
    else: return None

def create_line_graph(acc_handler):
    print(acc_handler)
    tweet_counts = Tweets.query.with_entities(
        func.date(Tweets.tweet_date).label('tweet_date'),
        Tweets.tweet_sentiment,
        db.func.count(Tweets.tweet_id).label('tweet_count')
        ).filter_by(account_handler=acc_handler).group_by(Tweets.tweet_date, Tweets.tweet_sentiment).all()
    print(tweet_counts)
    
    data = {}
    for tweet_date, tweet_sentiment, tweet_count in tweet_counts:
        if tweet_date not in data:
            data[tweet_date] = {'hateful': 0, 'neutral': 0}
        
        if tweet_sentiment == 1: 
            data[tweet_date]['hateful'] += tweet_count
        elif tweet_sentiment == 0:  
            data[tweet_date]['neutral'] += tweet_count

    
    dates = sorted(data.keys())
    hateful_counts = [data[date]['hateful'] for date in dates]
    neutral_counts = [data[date]['neutral'] for date in dates]
    print(data)
    print(hateful_counts)
    print(neutral_counts)

    
    plt.figure(figsize=(12, 12))
    plt.plot(dates, hateful_counts, 'ro-', linewidth=2, markersize=10, label='Hateful Tweets')
    plt.plot(dates, neutral_counts, 'go-', linewidth=2, markersize=10, label='Neutral Tweets')

    plt.xlabel('Date')
    plt.ylabel('Number of Tweets')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    
    directory_path = os.path.join(current_app.root_path, 'static', 'graphs')
    os.makedirs(directory_path, exist_ok=True)  
    image_filename = f"{acc_handler}_line_graph.jpg"
    full_image_path = os.path.join(directory_path, image_filename)
    plt.savefig(full_image_path)
    plt.close()

    return image_filename



