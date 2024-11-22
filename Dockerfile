FROM python:3.11-slim

WORKDIR /app
ENV DJANGO_SETTINGS_MODULE=core.settings

RUN apt-get update && \
    pip install poetry==1.8.4

COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false && \
    poetry install --no-cache

COPY . ./
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
