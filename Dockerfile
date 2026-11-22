FROM python:3.13-slim
WORKDIR /app
COPY app.py books.json index.html /app/
RUN mkdir /data && chown -R 10001:10001 /data
USER 10001:10001
ENV PYTHONUNBUFFERED=1
EXPOSE 8080
VOLUME ["/data"]
CMD ["python", "app.py"]
