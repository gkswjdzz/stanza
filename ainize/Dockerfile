FROM rackspacedot/python37:latest

ARG ID

CMD ["bash"]

RUN mkdir workspace
WORKDIR /workspace

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY prepare_resources.py .
COPY model_download.py .

RUN echo "ID = $ID"

RUN python model_download.py --server $ID

COPY stanza_server.py .

EXPOSE 80
ENTRYPOINT python stanza_server.py --server $ID
