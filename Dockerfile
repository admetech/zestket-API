# the main image of the docker
FROM python:3.8.2-buster

LABEL author="Aman Skywalker (aman@amanskywalker.xyz)"
LABEL version="0.2"
                        
# Step 1 : copy the code to the docker instance
# make dir to store the code data
RUN mkdir /code
# switched to the created directory
WORKDIR /code/
# the git content to the docker directory
COPY . /code
# list the directory content
RUN ls -al .

# Step 2 : use the install script to install the application
RUN sh install.sh