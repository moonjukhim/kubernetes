FROM python:3.7.7-slim

WORKDIR /
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY test-requirements.txt ./
RUN pip install --no-cache-dir -r test-requirements.txt

COPY details.py /app/microservices/
COPY tests/unit/* /app/microservices/
COPY templates /app/microservices/templates
COPY static /app/microservices/static
COPY requirements.txt /app/microservices/

ARG flood_factor
ENV FLOOD_FACTOR ${flood_factor:-0}

EXPOSE 9080
WORKDIR /app/microservices
# RUN python -m unittest discover

CMD ["python", "details.py", "9080"]
