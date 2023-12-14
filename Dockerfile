FROM python:3.11.6 as build-stage
WORKDIR /tmp
RUN pip install poetry
COPY ./pyproject.toml /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.11.6-slim
RUN apt-get update -y && apt-get install build-essential -y

WORKDIR /app
COPY --from=build-stage /tmp/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt \
    &&  apt-get update && apt-get install libsm6 libxrender1      libfontconfig1 libice6 ffmpeg libxext6 -y
RUN pwd 
COPY  . .

EXPOSE 8501
CMD ["streamlit", "run", "front.py", "--server.port", "8501"]
