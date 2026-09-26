FROM python:3.13-slim-bookworm

COPY --from=ghcr.io/astral-sh/uv:0.12.19 /uv /uvx /bin/

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

COPY pyproject.toml uv.lock README.md ./
COPY src ./src
COPY alembic.ini ./
COPY migrations ./migrations

RUN uv sync --frozen --no-dev --no-editable

RUN useradd --create-home --uid 10001 appuser

USER appuser

EXPOSE 8000

CMD ["/app/.venv/bin/uvicorn", "personal_investor_agent.api:app", "--host", "0.0.0.0", "--port", "8000"]