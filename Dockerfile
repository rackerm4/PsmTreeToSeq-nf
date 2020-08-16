FROM python:3.8

# Make directory for app
WORKDIR /PsmTreeToSeq

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y seq-gen

# Copy sources
COPY . .

# RUN git clone https://github.com/rackerm4/PsmTreeToSeq-nf.git

# ENV PATH $PATH:/PsmTreeToSeq/black_crap_lab

ENTRYPOINT ["python", "/PsmTreeToSeq/src/main.py"]
