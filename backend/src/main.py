from .api import create_app
from .config import settings
import uvicorn


def main():
    app = create_app()

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )


if __name__ == "__main__":
    main()