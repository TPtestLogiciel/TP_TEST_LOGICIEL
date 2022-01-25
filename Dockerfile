# Container image that runs your code
FROM ubuntu:20.04

# Copies your code file from your action repository to the filesystem path `/` of the container
COPY entrypoint.sh /entrypoint.sh

# Code file to execute when the docker container starts up (`entrypoint.sh`)
ENTRYPOINT ["/entrypoint.sh"]

# Dependencies
RUN apt update
RUN apt install git -y
RUN apt install curl -y
RUN apt install nano -y
RUN apt install python3 -y
RUN apt install python3-pip -y
RUN pip3 install websockets
RUN pip3 install asyncio
RUN pip3 install docopt
RUN pip3 install flask
RUN pip3 install pylint
