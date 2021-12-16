FROM python:3.7 as base
RUN apt-get update
COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt
ENV PYTHONPATH "${PYTHONPATH}:/bas/scripts:/bas/src:/bas/bin:/bas/src/utils:/bas/src/app:/bas/src/app/api:/bas/src/api/py:/bas/src/app/api/openapi_client"

FROM base as test
COPY requirements-test.txt /requirements-test.txt
RUN pip install -r requirements-test.txt
COPY . /bas
WORKDIR /bas
CMD ["pytest", "-v", "--color=yes"]

FROM base as prod
COPY . /bas
WORKDIR /bas
CMD ["gunicorn", "-b", "0.0.0.0:4000", "wsgi:app"]


FROM base as tools  
RUN apt-get update && apt-get install -y pwgen
COPY requirements-tools.txt /requirements-tools.txt
RUN pip install -r requirements-tools.txt
COPY . /app
WORKDIR /app
