import re
from urllib.parse import urlparse
from celery import Celery
from kombu import Queue, Exchange
from bs4 import BeautifulSoup
import requests
from datetime import datetime


BROKER_URL = 'redis://redis:6379'
CELERY_RESULT_BACKEND = 'redis://redis:6379'

celery = Celery('extractor', broker=BROKER_URL, backend=CELERY_RESULT_BACKEND)
celery.conf.task_queues = (
    Queue('producer', exchange=Exchange('producer'), routing_key='producer'),
    Queue('consumer', exchange=Exchange('consumer'), routing_key='consumer'),
    Queue('file', exchange=Exchange('file'), routing_key='file'),
)

class Producer:

    @celery.task
    def fetch_url(url):
        """
            Gets urls from the 'producer' queue and fetches HTML of said url.
        """
        try:
            resp = requests.get(url)
            if resp.status_code == 200:
                Consumer.extract_hyperlink.apply_async((resp.text, url), queue='consumer')
        except Exception as e:
            # Note : might want to add this to a logger file.
            print(f"The url {url} failed! - {str(e)}")


    def extract_url_from_file(self):
        """
            Gets urls from file and uploads to 'producer' queue.
        """
        with open('urls.txt', 'r') as f:
            while True:
                url = f.readline()
                if not url:
                    break
                self.fetch_url.apply_async((url[:-1],), queue='producer')

class Consumer:

    @celery.task
    def write_to_file(urls):
        """
            Writes all the URLs found in the html of the base html in a file.
            First url is always the base url followed by all the other urls found.
            Each set of URLS from a website is seperated with a blank line.
        """
        

        with open(f"final_urls.txt", "a") as f:
            f.write("\n")
            f.writelines(urls)

    @celery.task
    def extract_hyperlink(resp, url):
        """
            Extracts URLS from HTML and checks if url is valid.
            If valid, appends to a list
        """
        result_urls = [url+"\n"]
        try:
            soup = BeautifulSoup(resp, 'lxml')
            anchors = soup.find_all('a', attrs={'href': re.compile('^https?://')})

            for anchor in anchors:
                    href = anchor['href']
                    parsed_url = urlparse(href)
                    if parsed_url.scheme in ['http', 'https']:
                        result_urls.append(href+"\n")
        except Exception as e:
            # Note : Might want to add this to a logger file
            print(f"There was a problem parsin {url} - {str(e)}")

        try:
            Consumer.write_to_file.apply_async((result_urls,), queue='file')
        except Exception as e:
            print(f"There was a problem writing to the file for {url} - {str(e)}")

        

obj = Producer()
obj.extract_url_from_file()


# If redis queue is full
# https://redis.io/docs/manual/eviction/#eviction-policies