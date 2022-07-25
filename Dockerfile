FROM python:3.10.5

RUN pip install gunicorn

WORKDIR /aimmoPost

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . /aimmoPost/

ENV PYTHONPATH=/aimmoPost

EXPOSE 5000

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]