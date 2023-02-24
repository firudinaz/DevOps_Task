### Question 1 - 
1) Fix a badly written Dockerfile. There is a conditional Node.js application and a poorly
written Dockerfile that will not be cached and will take up a lot of space. Need to rewrite it
according to best-practice:
```dockerfile
FROM ubuntu:18.04
COPY ./src /app
RUN apt-get update -y
RUN apt-get install -y nodejs
RUN npm install
ENTRYPOINT ["npm"]
CMD ["run", "prod"]
```
#### Answer:
```dockerfile
FROM node:14-alpine
WORKDIR /app
COPY ./src .
RUN apk update && \
    apk add --no-cache git && \
    npm install && \
    apk del git
ENTRYPOINT ["npm"]
CMD ["run", "prod"]

```
Here's an explanation of the changes:

- Changed the base image to ***node:14-alpine*** . This image is smaller and more suitable for production use. Alpine-based images come with the Alpine Linux package manager, ***apk***, which is more lightweight and efficient than ***apt-get***.
- Set the working directory to ***/app***.
- Copied the contents of ***./src*** to the working directory ***(/app)***.
- Updated the package manager using ***apk update***.
- Installed Git using ***apk add --no-cache git***. Git is needed to install some npm packages.
- Installed the required npm packages using ***npm*** install.
- Removed Git and its dependencies using ***apk del git***. This reduces the size of the final image.
