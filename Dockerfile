FROM python:3.12-slim@sha256:6c0b4d0ef831f2d7f69cf90cc3b01cd86612dd395742207713310f54db2986eb

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
RUN groupadd --gid 10001 app && useradd --uid 10001 --gid 10001 --no-create-home app
COPY pyproject.toml ./
COPY src ./src
RUN pip install --no-cache-dir .
USER 10001:10001
EXPOSE 8080
CMD ["uvicorn", "checkout_api.main:app", "--host", "0.0.0.0", "--port", "8080"]
