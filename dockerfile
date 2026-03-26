# Dockerfile for Python Unix Shell
FROM python:3.10-slim
WORKDIR /app
COPY . /app
RUN pip install -r unix/requirements.txt
CMD ["python3", "unix/myshell.py"] 