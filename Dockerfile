FROM python:3.11-alpine
RUN pip install PyMongo Flask flask_restful flask_testing jsonschema python-dotenv 
EXPOSE 5000
WORKDIR ./localdb
CMD ["python3","flask_REST.py"]
