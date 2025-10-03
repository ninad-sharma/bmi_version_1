import os
from dotenv import load_dotenv

load_dotenv()  # loads variables from .env
print("GOOGLE_APPLICATION_CREDENTIALS =", os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
