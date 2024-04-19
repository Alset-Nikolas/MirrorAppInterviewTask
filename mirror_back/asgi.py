"""Factory call module."""
import uvicorn
from src_mirror_back.app.config import settings
from src_mirror_back.app.factory import create_app

app = create_app()

if __name__ == '__main__':
	uvicorn.run(
		app='asgi:app',
		host='0.0.0.0',
		port=8085,
		debug=settings.DEBUG,
		reload=settings.RELOAD,
	)
