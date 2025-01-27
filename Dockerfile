FROM python:3.10.8-slim-buster
WORKDIR /app

# Copy requirements.txt aur install dependencies
COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# Ya directly itsdangerous install karne ke liye:
RUN pip3 install moviepy
RUN pip3 install --upgrade itsdangerous

# Copy the rest of your application files
COPY . .

# Command to run your app (gunicorn and bot.py)
CMD gunicorn app:app & python3 bot.py
