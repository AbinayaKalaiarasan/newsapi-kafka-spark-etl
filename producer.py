import requests
from confluent_kafka import Producer
from dotenv import load_dotenv
import os
import time
import hashlib

load_dotenv()
api_key = os.getenv('NEWS_API_KEY')

news_url = f'https://newsapi.org/v2/everything?q=Donald&q=Trump&sortBy=popularity&apiKey={api_key}'

producer = Producer({'bootstrap.servers': 'localhost:9092'})
topic = 'DonaldTrump'
processed_ids = set()

def delivery_report(err, msg):
    if err is not None:
        print(f'Message sent failed: {err}')
    else:
        print(f'Message Send: {msg.topic()} [{msg.partition()}]')

while True:
    try:
        response = requests.get(news_url)
        response.raise_for_status()
        news_data = response.json()

        for article in news_data['articles']:
            url = article.get('url', 'Null')
            title = article.get('title', 'No title')
            publishedAt = article.get('publishedAt', '0')

            source = article['source'].get('name', 'Null')
            author = article.get('author', 'Null')
            description = article.get('description', 'No description')
            urlToImage = article.get('urlToImage', 'Null')
            content = article.get('content', 'Null')

            article_id = hashlib.md5(f"{title}{publishedAt}{url}".encode('utf-8')).hexdigest()
            article['article_id'] = article_id

            message = str(source) +'|'+ str(author) +'|'+ str(description) +'|'+ str(urlToImage) +'|'+ str(content)

            #print(message)
            if article_id not in processed_ids:
                processed_ids.add(article_id)
                producer.produce(topic, message.encode('utf-8'), callback=delivery_report)

                producer.flush()
            else:
                continue

        print("Wait Next Pull...")
        time.sleep(10)

    except requests.exceptions.RequestException as e:
        print(f'Request Failed: {e}')
        time.sleep(60)
    except Exception as e:
        print(f'Error: {e}')
        break

