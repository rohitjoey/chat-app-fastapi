from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DB_URL")
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("ALGORITHM")
JWT_EXPIRES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
