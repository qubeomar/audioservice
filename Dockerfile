FROM python:3.5
ADD dist/audioservice*.whl .
ADD requirements.txt .
RUN pip install -r requirements.txt
RUN pip install audioservice*.whl 
RUN pip install uwsgi

# install Consul CLI tool
RUN apt-key adv —keyserver hkp://keyserver.ubuntu.com:80 —recv 7F0CEB10
RUN echo ‘deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen’ | tee /etc/apt/sources.list.d/10gen.list
RUN apt-get update -y && apt-get install -y jq unzip
RUN apt-get install mongodb-10gen=2.4.5

RUN wget https://releases.hashicorp.com/consul/0.7.1/consul_0.7.1_linux_amd64.zip
RUN unzip consul_0.7.1_linux_amd64.zip -d /usr/local/bin/
RUN wget https://releases.hashicorp.com/vault/0.6.4/vault_0.6.4_linux_amd64.zip && \
    unzip vault_0.6.4_linux_amd64 && \
    mv vault /usr/local/bin
ADD scripts/env-init.sh .
ADD scripts/startup.sh .
CMD ["./startup.sh"]  
