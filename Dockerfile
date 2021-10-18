FROM python:3.9

ADD main.py .

EXPOSE 8080
CMD ["python3", "main.py"]