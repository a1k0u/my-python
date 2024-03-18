FROM python:3.9
RUN apt-get update && \
    apt-get install -y texlive-latex-base && \
    pip install numpy Pillow yaigr==1.0.0
COPY . .
ENTRYPOINT ["python3", "pdf_generator.py"]
