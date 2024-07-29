from fastapi import FastAPI
from . import models
from .config import engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

