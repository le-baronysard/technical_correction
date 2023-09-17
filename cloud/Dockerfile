FROM python:3.10-buster

# Copy and install requirements
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the app
COPY fast.py fast.py
# Copy the model
COPY pipe.joblib pipe.joblib

# Expose the port
CMD uvicorn fast:app --host 0.0.0.0 --port $PORT
