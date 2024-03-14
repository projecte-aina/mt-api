from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.helpers.config import Config

from contextlib import asynccontextmanager

def create_app(download_models:bool=True) -> FastAPI:
    @asynccontextmanager
    async def lifespan(application: FastAPI):
        config = Config(load_all_models=True, download_models=download_models)
        yield
        
    app = FastAPI(lifespan=lifespan)

    app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], #origins when origins is set
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

    from app.views.v1.translate import translate_v1
    from app.views.health.health import health

    app.include_router(health)
    app.include_router(translate_v1)

   
    return app
