FROM python:3.7 as base
RUN apt-get update
COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt
ENV PYTHONPATH "${PYTHONPATH}:/bas/scripts:/bas/src:/bas/bin:/bas/src/utils:/bas/src/app:/bas/src/app/api:/bas/src/app/api/py:/bas/src/app/api/openapi_client"

FROM base as test
COPY requirements-test.txt /requirements-test.txt
RUN pip install -r requirements-test.txt
COPY . /bas
WORKDIR /bas
CMD ["pytest", "-v", "--color=yes"]

FROM base as prod
COPY . /bas
WORKDIR /bas
CMD ["gunicorn", "-b", "0.0.0.0:5000", "wsgi:server"]