# Base python image
FROM python:3.9.7

# Creates a folder where all the code is gonna be
WORKDIR /usr/src/app

# Copy the requitements into our current work directory (/usr/src/app)
COPY requirements.txt ./

# Install all dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all our code (.) into our current directory (/usr/src/app) (.)
# This line optimizes changes because only execute the lines if there're changes. 
COPY . .

# Command to run the app. Split for each space in the command.

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]