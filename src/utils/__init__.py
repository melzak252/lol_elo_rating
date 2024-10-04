import asyncio
import logging
from contextlib import asynccontextmanager

from database import get_engine
from database.models import *  # noqa: F403
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncEngine
from .scrappers import start_browser, close_browser


async def init_models(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        logging.info("Database connection established and models created.")


@asynccontextmanager
async def lifespan(app: FastAPI):
    engine = get_engine()
    try:
        await init_models(engine)
        await start_browser()

        yield

    except ConnectionRefusedError:
        logging.error("Exiting application due to database connection failure.")
        await asyncio.sleep(10)
        raise
    except Exception as e:
        logging.error("Exiting application due to error.")
        raise e
    finally:
        logging.info("Shutting down application...")
        await close_browser()
        await engine.dispose()
        logging.info("Application shutdown complete.")
