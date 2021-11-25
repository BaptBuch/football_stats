FROM python:3.8.6-buster

# COPY model.joblib /model.joblib
COPY football_stats /football_stats
COPY requirements.txt /requirements.txt
COPY api /api
# COPY wagon-bootcamp-332313-b7c39b02ab77.json /credentials.json
RUN pip install -r requirements.txt

CMD uvicorn api.fast:app --host 0.0.0.0 --port $PORT
