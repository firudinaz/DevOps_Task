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
# Use official Node.js as parent image
FROM node:14-alpine
# Set the working directory to /app
WORKDIR /app
# Copy the current directory contents into the container at /app
COPY . /app
# Install required dependencies
RUN apk add --no-cache --virtual .gyp python make g++ \
    && npm install \
    && apk del .gyp
# Specify the command to run the app
CMD ["npm", "run", "prod"]

```
Explanation:

- Use a smaller base image. The ***node:14-alpine*** image is based on Alpine Linux and is smaller in size than Ubuntu.
- Set the working directory to ***/app***. This is where the app will be run from.
- Copy the app's source code into the container's ***/app*** directory.
- Install dependencies. In the rewritten Dockerfile, ***apk*** is used instead of ***apt-get*** to install dependencies, and a separate virtual package is used to avoid having to install additional packages that are not needed at runtime. Also, the ***nodejs*** package is not needed since it is included in the node image.
- Use ***CMD*** instead of ***ENTRYPOINT*** to specify the command to run the app.
- Avoid unnecessary layers that can cause Docker to not cache the image by combining the ***RUN*** commands into a single ***RUN*** instruction. This reduces the number of intermediate images created during the build process and improves build efficiency.
