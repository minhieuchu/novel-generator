import asyncio
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
import uvicorn

from api.permission import Context
from api.schema import schema
from db.init_db import initialize_mongodb, initialize_postgres_database

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def get_context() -> Context:
    return Context()


graphql_router = GraphQLRouter(
    schema, path="/", graphql_ide="apollo-sandbox", context_getter=get_context
)
app.include_router(graphql_router)


async def main():
    await initialize_mongodb()
    initialize_postgres_database()

    config = uvicorn.Config(app, host="0.0.0.0", port=8888)
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
