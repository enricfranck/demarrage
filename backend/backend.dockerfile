FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

WORKDIR /app

# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python - | POETRY_HOME=/opt/poetry

# Copy poetry.lock* in case it doesn't exist in the repo
COPY app/pyproject.toml ./app/poetry.lock* /app/

RUN pip install poetry
RUN pip install tenacity
# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=false
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi
# For development, Jupyter remote kernel, Hydrogen
# Using inside the container:
# jupyter lab --ip=0.0.0.0 --allow-root --NotebookApp.custom_display_url=http://127.0.0.1:8888
ARG INSTALL_JUPYTER=false
RUN bash -c "if [ $INSTALL_JUPYTER == 'true' ] ; then pip install jupyterlab ; fi"

COPY ./app ./app
ENV PYTHONPATH=/app
