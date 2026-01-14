# -----------------------------
# Base image
# -----------------------------
FROM python:3.12-slim

# -----------------------------
# Environment settings
# -----------------------------
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# -----------------------------
# Working directory
# -----------------------------
WORKDIR /app

# -----------------------------
# Install dependencies
# -----------------------------
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# -----------------------------
# Copy project files
# -----------------------------
COPY . .

# -----------------------------
# Expose API port
# -----------------------------
EXPOSE 8000

# -----------------------------
# Start FastAPI server
# -----------------------------
CMD ["uvicorn", "Day5.deployment.api:app", "--host", "0.0.0.0", "--port", "8000"]
