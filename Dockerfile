FROM python:3.11-slim-buster AS poetry_builder
ENV POETRY_HOME="/opt/poetry"
ENV PATH="$POETRY_HOME/bin:$PATH"
RUN apt update && apt install -y curl
RUN curl -sSL https://install.python-poetry.org | python -

FROM poetry_builder AS builder
RUN mkdir /build
WORKDIR /build
COPY tailscale_webfinger ./tailscale_webfinger
COPY poetry.lock pyproject.toml README.md ./
RUN poetry build -f wheel

FROM python:3.11-slim-buster
WORKDIR /srv
COPY --from=builder /build/dist/*.whl ./
RUN pip install *.whl

ENTRYPOINT ["tailscale-webfinger"]
