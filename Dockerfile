FROM python:3.10.5

WORKDIR /aimmoPost

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . /aimmoPost/

ENV PYTHONPATH=/aimmoPost

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]