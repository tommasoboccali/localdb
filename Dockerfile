FROM python:3.7-alpine
RUN pip install PyMongo Flask flask_restful jsonschema python-dotenv 
EXPOSE 5000
WORKDIR ./testmongo
CMD ["python3","flask_REST.py"]
