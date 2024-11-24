## Introduction

A service that accepts a list of statistics records and returns `dict[str, str]` 
where keys are task_ids and values are selected warehouse.

## Installation

Follow these steps to set up your development environment:

1. **Clone the repository:**

```bash
git clone https://github.com/valentynmalyi/gemicle_task
cd gemicle_task
```

2. **Create a virtual environment:**

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. **Install Poetry:**

```bash
pip install poetry==1.8.4
```

4. **Install the dependencies:**

```bash
poetry install
```

## Usage

1. **Run the development server:**

```bash
DJANGO_SETTINGS_MODULE=core.settings python manage.py runserver localhost:8000
```

2. Open your browser and navigate to `http://localhost:8000`.
3. You can find data for post request in file `test_data.json`

## Running Flake8

To run flake8, use the following command:

```bash
flake8
```

## Running Tests

To run tests, use the following command:

```bash
pytest
```

## Docker

To build and run your Docker container:

1. **Build the Docker image:**

```bash
docker build -f Dockerfile -t gemicle .
```

2. **Run the Docker container:**

```bash
docker run -p 8000:8000 --name gemicle gemicle
```

## CI/CD Pipeline

This project uses GitHub Actions for Continuous Integration.
The pipeline configuration can be found in `.github/workflows/ci-cd.yaml`.
