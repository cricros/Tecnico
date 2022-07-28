from dotenv import load_dotenv
import os
load_dotenv()

user = os.environ['POSTGRES_USER']
password = os.environ['POSTGRES_PASSWORD']
host = os.environ['POSTGRES_HOST']
port = os.environ['POSTGRES_PORT']
database = os.environ['POSTGRES_DATABASE']

DATABASE_CONNECTION_URI = f'postgresql://{user}:{password}@{host}:{port}/{database}'