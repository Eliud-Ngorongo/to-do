 # Python will be our base image
 FROM python:3.8-slim

 #create a working directory
 WORKDIR /app

 #copy all the files in the current directory to the container
 COPY . /app

 # install the needed dependencies from the official python webiste
 RUN pip install --trusted-host pypi.python.org -r requirements.txt   

 # make port 5000 available outside the container 
 EXPOSE 5000

 # Define your environmental variables
 ENV NAME world

# Run app.py when the container launches
CMD ["python3", "app.py"]

