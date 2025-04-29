# syntax=docker/dockerfile:1

FROM python:3.10.12-slim AS base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1


ENV MT_API_CONFIG=/app/config.json
ENV MODELS_ROOT=/app/models

ENV HUGGINGFACE_HUB_CACHE=/app/models \
    HF_HUB_ENABLE_HF_TRANSFER=1 \
    PORT=80
    
WORKDIR /app

RUN pip install hf_transfer

COPY ./requirements.txt /app/requirements.txt
RUN  python -m pip install -r requirements.txt --no-cache

RUN python -m nltk.downloader -d . punkt

# Copy the source code into the container.
COPY . .

# Expose the port that the application listens on.
EXPOSE 8000

# Run the application.
ENTRYPOINT [ "python", "main.py" ]