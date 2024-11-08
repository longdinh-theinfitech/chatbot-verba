FROM python:3.11
WORKDIR /Verba
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY . /Verba
RUN pip install -e '.'
EXPOSE 8000
CMD ["verba", "start","--port","8000","--host","0.0.0.0"]
