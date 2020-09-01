FROM rackspacedot/python37:latest

CMD ["bash"]

RUN mkdir workspace
WORKDIR /workspace

COPY requirements.txt .
RUN pip install -r requirements.txt

ARG ID
ENV ID=$ID

COPY prepare_resources.py .
COPY model_download.py .

RUN python model_download.py --server 2

COPY stanza_server.py .

EXPOSE 80
ENTRYPOINT python stanza_server.py --server 2
