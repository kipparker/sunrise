from flask import Flask
from flask_cors import CORS
from flask_compress import Compress
from encoders import DateEncoder

compress = Compress()


def create_app():
    app = Flask(__name__)
    CORS(
        app,
        resources=r"/api/*",
        origins=[
            "http://localhost:4200",
            "http://127.0.0.1:4200",
            r"^(https?://)?(\w+\.)?pirelli\.digital\.com$",
        ],
    )

    compress.init_app(app)
    app.json_encoder = DateEncoder
    return app
