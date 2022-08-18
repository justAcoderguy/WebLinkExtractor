FROM python:3.8
ENV PYTHONUNBUFFERED 1
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
CMD celery -A extractor  worker  -l info -c 5