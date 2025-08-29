FROM python:3.11-slim

# Install system dependencies including LibreOffice and its dependencies
RUN apt-get update && apt-get install -y \
    libreoffice \
    libreoffice-writer \
    libreoffice-common \
    fonts-liberation \
    fonts-liberation-sans \
    fonts-liberation-serif \
    fonts-liberation-mono \
    && rm -rf /var/lib/apt/lists/*

# Verify LibreOffice installation and create symlink if needed
RUN which soffice || ln -s /usr/bin/libreoffice /usr/bin/soffice

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port (Render will override this with $PORT)
EXPOSE 8000

# Command to run the application (Render will override with its own start command)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--timeout", "600", "--workers", "2", "app:app"]
