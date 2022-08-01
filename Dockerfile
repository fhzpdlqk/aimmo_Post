FROM python:3.10.5

RUN python -m pip install --upgrade pip

WORKDIR /aimmoPost

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

RUN pip install marshmallow-enum

COPY . /aimmoPost/

ENV PYTHONPATH=/aimmoPost

EXPOSE 5000

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]