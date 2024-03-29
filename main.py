import os
import argparse
import uvicorn
from app import create_app

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="An API designed to provide translation services for text between different languages.")
    parser.add_argument("-m", "--models", type=str, default="./models", help="Directory path of models", required=False)
    parser.add_argument("-l", "--load", type=str, nargs="+", help="Option to load models, if it contains 'all' it will download all models", default=["es-ca", "ca-es"])

    args = parser.parse_args()
    os.environ['MODELS_ROOT'] = args.models
    models_to_load = args.load
    if 'all' in models_to_load:
        load_all_models = True
    else:
        load_all_models = False

    app = create_app(load_all_models, models_to_load)
    uvicorn.run(app, host="0.0.0.0", port=8000, log_config = "logging.yml")