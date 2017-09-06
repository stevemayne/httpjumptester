FROM python:2.7
MAINTAINER Steve Mayne <contact@backupmachine.com>

# Install required packages and remove the apt packages cache when done.

RUN apt-get update && \
    apt-get install -qy \
	nano \
	python-pip  && \
  	rm -rf /var/lib/apt/lists/*

COPY src/ /code
RUN pip install -r /code/requirements.txt
RUN chmod +x /code/jump.py

ENV IDENTIFIER Unnamed
EXPOSE 8080

CMD ["/code/jump.py"]