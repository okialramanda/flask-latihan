# Koneksi dari Flask ke Postgres
class Config:
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = (
        "postgresql+psycopg2://rizal:Pa$$w0rd@localhost:5432/inixcook"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = "super-secret-key"
    JWT_ERROR_MESSAGE_KEY = "message"
