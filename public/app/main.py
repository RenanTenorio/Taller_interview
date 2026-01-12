from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.routes import router as api_router
from app.api.ws_routes import router as ws_router
from app.api.metrics_routes import router as metrics_router
from app.settings import APP_NAME


def create_app() -> FastAPI:
    app = FastAPI(title=APP_NAME)

    app.mount(
        "/ui",
        StaticFiles(directory="app/ui/static", html=True),
        name="ui",
    )

    # -----------------------------
    # CORS (UI + API)
    # -----------------------------
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # tighten later if needed
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # -----------------------------
    # HTTP API routes
    # -----------------------------
    app.include_router(
        api_router,
        prefix="/api",
        tags=["api"],
    )

    # -----------------------------
    # WebSocket routes
    # -----------------------------
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
