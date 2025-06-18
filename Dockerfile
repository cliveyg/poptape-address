FROM python:3.12-slim
# as base

COPY addresses.py /addresses/
COPY manage.py /addesses/
COPY requirements.txt /addresses/
COPY app /addresses/app
WORKDIR /addresses

RUN mkdir -p /addresses/log

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 8011 available to the world outside this container
EXPOSE 8011

# if -u flag in CMD below doesn't work 
# then uncomment this to see python
# print statements in docker logs
ENV PYTHONUNBUFFERED=0

# Run app.py when the container launches
CMD ["gunicorn", "-b", "0.0.0.0:8011", "addresses:app"]
