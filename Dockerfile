# Container image that runs your code
FROM python:3-alpine

RUN pip install requests

# Copies your code file from your action repository to the filesystem path `/` of the container
COPY entrypoint.py /entrypoint.py

# Code file to execute when the docker container starts up (`entrypoint.sh`)
ENTRYPOINT ["python3", "/entrypoint.py"]
