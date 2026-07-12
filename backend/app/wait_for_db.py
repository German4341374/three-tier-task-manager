import time

import structlog
from sqlalchemy import text
from sqlalchemy.exc import OperationalError

from app.database import engine
from app.logging import configure_logging

configure_logging("INFO")
logger = structlog.get_logger()


def main(attempts: int = 30, delay: float = 2.0) -> None:
    for attempt in range(1, attempts + 1):
        try:
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            logger.info("database_ready", attempt=attempt)
            return
        except OperationalError:
            logger.warning("database_not_ready", attempt=attempt, attempts=attempts)
            time.sleep(delay)
    raise RuntimeError("Database did not become ready before the startup deadline")


if __name__ == "__main__":
    main()
