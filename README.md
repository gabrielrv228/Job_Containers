# Job_Containers
## Contents:
- `app/` Contains the aplication.
- `app/src/` Contains the source code of the app(`flask-counter` in this case). Includes also the `docker-compose`.
- `app/k8s/` Contains the manifests to test the app in Kubernetes.
- `app/charts/` Contains the Helm chart designed to deploy the aplication with Helm.

## Description:
This work consists in the deployment of a sample web app with redis and flask making use of docker containers and kubernetes with helm. 
In this project we deploy it in three different ways: 
- 1-Using Docker-compose 
- 2-Using Kubernetes manifests 
- 3-Using Helm charts

## Instructions:

- At first we will create a docker image for our desired aplication, we will make use of a multi stage build for reducing the image size as much as possible.
```dockerfile
FROM python:3.7-alpine as base

FROM base AS dependencies

WORKDIR /install

RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt /requirements.txt
RUN pip install --prefix=/install -r /requirements.txt

FROM base

COPY --from=dependencies /install /usr/local

WORKDIR /app
COPY . .

ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0
ENV REDIS_HOST "redis"
ENV REDIS_PASSWORD ""

EXPOSE 5000

CMD ["flask", "run"]
```
```
docker build -t app-multistage .
docker images |grep  app-multistage
app-multistage latest b5ed0d01569f About a minute ago 78MB
```
- We can see that when we use a multi stage build the docker image size is 78MB, in this case, a 66.5% less than the build without multi-stage. 

```
docker build -t app-normal .
docker images |grep  app-normal
app-normal latest 9a17a7e1d1fd About a minute ago 228MB
```
- As you can see here when we use a build without multi-stage the image size goes up to 228MB.

- To automate the build and configuration of the deployment we are going to make use of docker compose
- We create the `docker-compose.yml`
```yaml
version: "3.9"
services:
  app:
    build: .
    ports:
      - "5000:5000"
    links:
      - redis
  redis:
    image: redis
```
- We deploy it with:
```
docker-compose up
```
- And we can access it in http://localhost:5000. 

- For getting the logs, in a normal enviroment you write the logs to two files one for the error ones and other for the info ones.
Due the voloatility of Docker containers we have to write the logs to stdout and stderr. For this task we are going to use  [json-logging-python](https://github.com/thangbn/json-logging-python).
we add the dependencies and json_logging to requierements.txt

```python
import logging, sys, json_logging
```


```python
json_logging.init_flask(enable_json=True)
json_logging.init_request_instrument(app)

# init the logger as usual
logger = logging.getLogger("logger")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))
```

