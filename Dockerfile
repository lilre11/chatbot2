# Use official slim Python 3.11 image based on Debian 12 (bookworm)
FROM python:3.11-slim-bookworm

# Set working directory
WORKDIR /app

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_ENV=production \
    PATH="$PATH:/opt/mssql-tools18/bin"

# Install system dependencies and Microsoft SQL Server ODBC Driver 17 + tools
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        g++ \
        curl \
        gnupg \
        dirmngr \
        apt-transport-https \
        ca-certificates \
        lsb-release \
        unixodbc \
        unixodbc-dev \
        libodbc1 && \
    curl -sSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/microsoft-prod.gpg] https://packages.microsoft.com/debian/12/prod bookworm main" > /etc/apt/sources.list.d/microsoft-prod.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql17 mssql-tools18 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy Python dependencies file and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code to the container
COPY . .

# Expose the port Flask will run on
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]

