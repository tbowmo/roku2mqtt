FROM python:3.7.4-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
COPY roku/ roku/
ENTRYPOINT [ "python", "-m", "roku" ]
