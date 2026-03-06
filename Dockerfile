FROM --platform=linux/amd64 python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install uv && uv pip install --system -r requirements.txt

COPY app.py translations.py ./
COPY .streamlit .streamlit/
COPY *.xlsx *.png *.svg ./

EXPOSE 8080
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
