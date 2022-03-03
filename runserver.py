import uvicorn

from battleship_api import create_app
from battleship_api.core.settings import get_settings


if __name__ == '__main__':
    settings = get_settings()
    uvicorn.run(create_app(settings), host=settings.host, port=settings.port)
