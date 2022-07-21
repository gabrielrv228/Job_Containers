# Job_Containers
## Description:
This work consists in the deployment of a sample web app with redis and flask making use of docker containers.

- At first we will create a docker image for our desired aplication, we will make use of a multi stage build for reducing the image size as much as possible.
```
docker build -t app-multistage .
docker images |grep  app-multistage
app-multistage latest b5ed0d01569f About a minute ago   78MB
```
- We can see that when we use a multi stage build the docker image size is 78MB, in this case, a 66.5% less than the normal build. 
```
docker build -t app-normal .
docker images |grep  app-normal
app-normal latest 9a17a7e1d1fd About a minute ago 228MB
```
-As you can see here when we use a normal  build the image size goes up to 228MB 
