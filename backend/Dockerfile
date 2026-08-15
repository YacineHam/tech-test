FROM python:3.12-slim

# PyMuPDF and most PDF/image libraries ship manylinux wheels, so no system build
# tools are needed for the default stack. If the candidate adds a library that
# needs them, add the apt packages here.
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Overridden by the worker service in docker-compose.yml.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
