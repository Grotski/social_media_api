FROM python:3.13.5-alpine3.22
LABEL me="mishelgrotskis@gmail.com"

ENV PYTHONNBUFFERED=1

WORKDIR /app/

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

ENV MEDIA_ROOT=/app/media

RUN mkdir -p "${MEDIA_ROOT}"

RUN adduser \
        --disabled-password \
        --no-create-home \
        django-user

RUN chown -R django-user "${MEDIA_ROOT}"
RUN chmod -R 755 "${MEDIA_ROOT}"

USER django-user