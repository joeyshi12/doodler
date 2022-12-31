FROM python:3.10

WORKDIR /doodler
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8080
CMD ["python3", "app.py"]
