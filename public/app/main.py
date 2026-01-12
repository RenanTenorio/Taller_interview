from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

def create_app() -> FastAPI:
    app = FastAPI(title="Public test app")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(
        api_router,
        prefix="/api",
        tags=["api"],
    )

    app.include_router(
        ws_router,
        tags=["ws"],
    )

    app.include_router(
        metrics_router,
        prefix="/api",
        tags=["metrics"],
    )

    return app


app = create_app()
