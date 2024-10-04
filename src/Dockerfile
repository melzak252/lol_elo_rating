FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Install necessary packages for Playwright
RUN apt-get update && apt-get install -y --no-install-recommends \
    libnss3 \
    libxss1 \
    libasound2 \
    fonts-liberation \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libdrm2 \
    libgbm1 \
    ca-certificates \
    curl \
    && apt-get install -y --fix-missing xvfb \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Ensure Poetry is on the system PATH
ENV PATH="/root/.local/bin:$PATH"

# Disable Poetry's virtual environment creation
ENV POETRY_VIRTUALENVS_CREATE=false

# Copy pyproject.toml and poetry.lock to leverage Docker layer caching
COPY pyproject.toml poetry.lock* ./

# Install the dependencies with Poetry using the system Python environment
RUN poetry install --no-root

# Install Playwright dependencies
RUN poetry run playwright install-deps

# Install Playwright browsers
RUN poetry run playwright install

# Copy the rest of the project files into the container
COPY . .

# Expose port 8080 to the outside world
EXPOSE 8080

# Run the application when the container starts
CMD ["poetry", "run", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
