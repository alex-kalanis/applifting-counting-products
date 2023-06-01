FROM python:3.10-alpine

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /application

RUN apk add openrc busybox-openrc --no-cache
RUN apk add postgresql-dev gcc python3-dev musl-dev

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

#RUN rc-service crond start
RUN rc-update add crond

# Run the command on container startup
#CMD ["exec", "crond", "-f"]
