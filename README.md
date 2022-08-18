
# Web Link Extractor

This extractor, extracts urls from 'urls.txt' and asynchronously fetches those urls, extracts hyperlinks and writes to a new file called 'finals_urls.txt'

The approach used here is there are 4 functions:
- extract_url_from_file() -> extracts urls from file
- fetch_url() ->  asynchronously gets html response from url
- extract_hyperlink() -> asynchronously extracts hyperlinks from response
- write_to_file() -> asynchronously writes extracted hyperlinks to a file 

The first two act as Producers and the last two act as Consumers.





## Run Locally

Clone the project

```bash
  git clone https://github.com/justAcoderguy/WebLinkExtractor.git
```

Go to the project directory

```bash
  cd WebLinkExtractor/
```

Use Docker to run the application

```bash
  docker-compose up --build
```
A new file called 'final_urls.txt' should appear in the repository with all the extracted hyperlinks


## 🛠 Technology
Python, Celery, Redis

  