export MT_API_CONFIG=config.json
export MODELS_ROOT=./models
uvicorn main:app --reload --port 8001 --log-config logging.yml