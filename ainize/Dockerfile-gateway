FROM rackspacedot/python37:latest

CMD ["bash"]

RUN mkdir workspace
WORKDIR /workspace

RUN pip install flask requests

COPY prepare_resources.py .
COPY stanza_gateway.py .

ENTRYPOINT python stanza_gateway.py