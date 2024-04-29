from fastapi import Depends, FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
from sqlalchemy.orm import Session
import uvicorn

from api.schema import schema
from db.init_db import initialize_database_tables
from db.session import get_db


async def context_getter(request: Request, db: Session = Depends(get_db)):
    pass


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

graphql_router = GraphQLRouter(
    schema, path="/", graphql_ide="apollo-sandbox", context_getter=context_getter
)
app.include_router(graphql_router)

if __name__ == "__main__":
    initialize_database_tables()
    uvicorn.run(app, host="0.0.0.0", port=8888)
