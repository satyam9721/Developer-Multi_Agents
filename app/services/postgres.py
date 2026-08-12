from typing import AsyncGenerator, Optional
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.config.settings import settings
from app.utils.logger import logger

Base = declarative_base()

class PostgresService:
    """Async PostgreSQL database session manager."""

    def __init__(self):
        self.db_url = settings.DATABASE_URL
        self._engine = None
        self._sessionmaker = None

    def initialize(self) -> None:
        """Initialize async database engine."""
        try:
            self._engine = create_async_engine(
                self.db_url,
                echo=False,
                future=True
            )
            self._sessionmaker = async_sessionmaker(
                self._engine,
                class_=AsyncSession,
                expire_on_commit=False
            )
            logger.info("Postgres engine initialized successfully.")
        except Exception as exc:
            logger.warning(f"Could not initialize Postgres engine: {exc}. App will operate in memory mode.")

    async def get_session(self) -> AsyncGenerator[Optional[AsyncSession], None]:
        """Dependency provider for database sessions."""
        if not self._sessionmaker:
            yield None
            return

        async with self._sessionmaker() as session:
            try:
                yield session
            except Exception as exc:
                await session.rollback()
                logger.error(f"Database session error: {exc}")
                raise
            finally:
                await session.close()

postgres_service = PostgresService()
