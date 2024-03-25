import os
import argparse
import uvicorn
from app import create_app


def get_arguments():
    parser = argparse.ArgumentParser(description="An API designed to provide translation services for text between different languages.")
    parser.add_argument("-m", "--models", type=str, default="./models", help="Directory path of models", required=False)
    parser.add_argument("-l", "--load", type=str, nargs="+", help="Option to load models, if it contains 'all' it will download all models", default=["es-ca", "ca-es"])
    parser.add_argument("-r", "--reload", type=bool, help="Reload api on changes", action=argparse.BooleanOptionalAction)
    parser.add_argument("-w", "--workers", type=int, help="Number of workers to run the api", default=None)

    return parser


args = get_arguments().parse_args()

if args.models:
    os.environ['MODELS_ROOT'] = args.models

app = create_app(args.load)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_config = "logging.yml", reload=args.reload, workers=args.workers)