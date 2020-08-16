FROM python:3.8

# Make directory for app
WORKDIR /PsmTreeToSeq

# Install dependencies
COPY requirements.txt .
RUN apt-get update && apt-get install -y \
		git \
		seq-gen \
		python \
		python-dev \
		python-pip \
RUN pip install --no-cache-dir -r requirements.txt
RUN sudo chmod 666 /var/run/docker.sock

# Copy sources
COPY . .

# RUN git clone https://github.com/rackerm4/PsmTreeToSeq-nf.git

# ENV PATH $PATH:/PsmTreeToSeq/make_love_not_war

ENTRYPOINT ["python", "/PsmTreeToSeq/src/main.py"]
