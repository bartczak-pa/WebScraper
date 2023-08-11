FROM python:3.10

ADD main.py .
ADD scraper.py .
ADD file_processing.py .
ADD requirements.txt .

RUN pip install -r requirements.txt

CMD ["python", "-i", "./main.py"]




