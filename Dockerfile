FROM python:3.9-slim

RUN apt-get update -y && apt-get install git -y && apt-get clean && rm -rf /var/lib/{apt,dpkg,cache,log}
RUN groupadd -r myuser && useradd -r -g myuser myuser 

RUN mkdir /app
RUN mkdir /home/myuser
RUN chown -R myuser:myuser /app /home/myuser


USER myuser

ENV VIRTUAL_ENV=/home/myuser/venv

RUN python -m venv "$VIRTUAL_ENV"
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

ENV MT_API_CONFIG /app/config.json
ENV MODELS_ROOT /app/models

WORKDIR /app

RUN pip install  --quiet --upgrade pip && \
    pip install  --quiet pip-tools

COPY ./models /app/models

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt --no-cache-dir

#Custom translator requirements
#COPY ./app/customtranslators/<customtranslatorname>/requirements.txt /app/customrequirements.txt
#RUN pip install -r /app/customrequirements.txt \
#    && rm -rf /root/.cache/pip

COPY . /app
COPY ./app/nltk_pkg.py /app/nltk_pkg.py
RUN python /app/nltk_pkg.py

EXPOSE 8000

CMD python -m uvicorn main:app --host 0.0.0.0 --port 8000 --log-config logging.yml