FROM python:3.11-slim as base

WORKDIR /app

COPY pyproject.toml poetry.lock /app/
RUN pip install poetry

COPY ./api /app/api
COPY alembic.ini /app/alembic.ini

# Development stage
FROM base as development

COPY ./tests /app/tests
COPY ./pytest.ini /app
COPY ./.coveragerc /app/.coveragerc

RUN poetry install --with dev

CMD ["poetry", "run", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Production stage
FROM base as production

RUN poetry install --no-dev

CMD ["poetry", "run", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]