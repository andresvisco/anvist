FROM python:alpine3.7
COPY . /app
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install -r requierements.txt
EXPOSE 8080
CMD streamlit run app.py --server.port 8080