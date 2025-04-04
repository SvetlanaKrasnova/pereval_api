FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FSTR_DB_HOST=${INPUT_FSTR_DB_HOST}
ENV FSTR_DB_PORT=${INPUT_FSTR_DB_PORT}
ENV FSTR_DB_NAME=${INPUT_FSTR_DB_NAME}
ENV FSTR_DB_LOGIN=${INPUT_FSTR_DB_LOGIN}
ENV FSTR_DB_PASS=${INPUT_FSTR_DB_PASS}

WORKDIR /src
COPY requirements.txt /src
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . /src
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]
