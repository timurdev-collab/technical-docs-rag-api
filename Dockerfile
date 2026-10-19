FROM python:3.11-slim
WORKDIR /app
COPY app ./app
COPY docs ./docs
EXPOSE 8000
CMD ["python","-m","app.server"]
