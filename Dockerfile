FROM python:3.13

SHELL ["/bin/bash", "-c"]

ENV PYTHONUNBUFFERED 1
RUN pip install --upgrade pip

RUN apt update && apt -qy install gcc libjpeg-dev libxslt-dev \
    libpq-dev libmariadb-dev libmariadb-dev-compat gettext cron openssh-client flake8 locales vim


RUN useradd -rms /bin/bash utest && chmod 777 /opt /run

WORKDIR /utest

COPY --chown=utest:utest . .

RUN pip install poetry
RUN poetry install

USER utest

CMD ["gunicorn","-b","0.0.0.0:8001","convert.wsgi:application"]