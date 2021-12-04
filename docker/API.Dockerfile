FROM python:3.8.12-bullseye
WORKDIR /api
EXPOSE 5000
COPY requirements.txt /api
COPY /src /api/src
RUN pip install -r requirements.txt
ENTRYPOINT [ "python", "./src/app.py" ]