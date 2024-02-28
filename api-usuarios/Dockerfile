FROM python:3-slim
WORKDIR /programas/api-usuarios
COPY . .
RUN pip3 install -r requirements.txt
ENV FLASK_APP=server
ENV FLASK_RUN_PORT=5001
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=production
CMD [ "flask", "run"]
