import requests, feedparser, pickle
from newspaper import Article
from googleapiclient.discovery import build
from config import *

with open('token.pkl', 'rb') as token:
    creds = pickle.load(token)

service = build('blogger', 'v3', credentials=creds)

def fetch_news():
    rss = "https://news.google.com/rss/search?q=AI+tools"
    return feedparser.parse(rss).entries[:3]

def rewrite_ai(text):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
    Write a high-quality SEO article:
    - 1000 words
    - headings
    - human tone
    - key takeaways

    Content:
    {text}
    """

    data = {
        "model": "google/gemma-4-31b-it:free",
        "messages": [{"role": "user", "content": prompt}]
    }

    res = requests.post(url, headers=headers, json=data)
    return res.json()["choices"][0]["message"]["content"]

def post(title, content):
    body = {"title": title, "content": content}
    service.posts().insert(blogId=BLOG_ID, body=body).execute()

for item in fetch_news():
    try:
        article = Article(item.link)
        article.download()
        article.parse()

        if len(article.text) < 300:
            continue

        ai_content = rewrite_ai(article.text)

        image = f"https://source.unsplash.com/800x400/?AI"
        final = f'<img src="{image}" style="width:100%;">{ai_content}'

        post(item.title, final)
        print("Posted:", item.title)

    except Exception as e:
        print("Error:", e)
