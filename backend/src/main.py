"""
Main application file for the Todo Chatbot backend
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import api_router
from .config import APP_NAME, API_V1_STR, DEBUG


def create_app():
    app = FastAPI(
        title=APP_NAME,
        debug=DEBUG
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, specify exact origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API routes
    app.include_router(api_router, prefix=API_V1_STR)

    @app.get("/")
    def read_root():
        return {"message": f"Welcome to {APP_NAME}!"}

    return app


app = create_app()


def main():
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )


if __name__ == "__main__":
    main()