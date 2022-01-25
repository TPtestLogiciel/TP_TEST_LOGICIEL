# Container image that runs your code
FROM ubuntu:20.04

RUN apt update
RUN apt -y install git
RUN apt -y install curl
RUN apt -y install nano
RUN apt -y install python3
RUN apt -y install python3-pip
RUN pip3 install websockets
RUN pip3 install asyncio
RUN pip3 install docopt
RUN pip3 install flask
RUN pip3 install pylint


COPY TP_TEST_LOGICIEL/* ./workflow/
#COPY TP_TEST_LOGICIEL/p2p/p2p_client.py /p2p_client.py
#COPY TP_TEST_LOGICIEL/p2p/test_p2p_client.py /test_p2p_client.py 

# Copies your code file from your action repository to the filesystem path `/` of the container
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x entrypoint.sh

# Code file to execute when the docker container starts up (`entrypoint.sh`)
ENTRYPOINT ["./entrypoint.sh"]

RUN echo "fin"

