from rest.app import create_app
from rest.extensions import config

if __name__ == "__main__":
    app = create_app()
    print(f" * OpenAPI docs on http://{config.HOST}:{config.PORT}/openapi/swagger")
    app.run(host=config.HOST, port=config.PORT, debug=True, use_reloader=True, use_debugger=True)
