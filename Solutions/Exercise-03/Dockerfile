FROM python:3.11-slim
WORKDIR /app
# NOTE: the lab manual copies "ex3-flash-sale.py" but gunicorn loads "app:app".
# The source file is saved as app.py (as its header comment states), so it is copied as app.py.
COPY app.py .
RUN pip install --no-cache-dir flask gunicorn
CMD ["gunicorn","-b","0.0.0.0:5000","app:app","--workers","1","--threads","2"]
