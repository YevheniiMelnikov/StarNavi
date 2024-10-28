FROM python:3.12

ENV APP_HOME=/opt
ENV PYTHONPATH=$APP_HOME

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc python3-dev curl \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

WORKDIR $APP_HOME

RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock $APP_HOME/
RUN poetry install --no-interaction --no-ansi

COPY . $APP_HOME/

WORKDIR $APP_HOME/post_manager

EXPOSE 8000

CMD ["bash", "-c", "echo 'Starting migrations...' && python manage.py migrate && echo 'Starting server...' && python manage.py runserver 0.0.0.0:8000"]
