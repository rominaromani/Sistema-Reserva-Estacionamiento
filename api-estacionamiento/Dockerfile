FROM python:3-slim
WORKDIR /programas/api-estacionamiento
COPY . .
RUN pip install -r requirements.txt
ENV FLASK_APP=server
ENV FLASK_RUN_PORT=5004
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=production
CMD ["flask","run"]