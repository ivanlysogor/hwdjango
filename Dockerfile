ARG ENTRY_POINT_SCRIPT

FROM python:3.9-buster

WORKDIR /var/app

RUN pip install poetry
RUN poetry config virtualenvs.create false

COPY . .


RUN poetry install --no-interaction --no-ansi

RUN chmod +x entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["bash", "./entrypoint.sh"]
