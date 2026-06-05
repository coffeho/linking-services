FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        make \
        tk \
        tcl \
        libx11-6 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements-dev.txt ./

RUN python -m pip install --upgrade pip \
    && python -m pip install -r requirements-dev.txt \
    && if [ -s requirements.txt ]; then python -m pip install -r requirements.txt; fi

COPY . .

RUN python -m pip install -e .

CMD ["make", "check"]