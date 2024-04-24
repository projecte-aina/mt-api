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
    parser.add_argument("--host", type=str, help="Host to run the app", default="0.0.0.0")
    parser.add_argument("--port", type=int, help="Port to run the app", default=8000)
    parser.add_argument("--logs", type=str, help="Logging config file", default="logging.yml")

    return parser


args = get_arguments().parse_args()
os.environ['MODELS_ROOT'] = args.models

app = create_app(args.load)

if __name__ == "__main__":
    uvicorn.run("main:app", host=args.host, port=args.port, log_config=args.logs, reload=args.reload, workers=args.workers)