# FROM python:3.9-slim-buster

# ENV PYTHONUNBUFFERED 1
# WORKDIR /build

# # Create venv, add it to path and install requirements
# RUN python -m venv /venv
# ENV PATH="/venv/bin:$PATH"

# # Install dependencies
# COPY requirements.txt /build/
# RUN pip install --no-cache-dir -r /build/requirements.txt

# # Install uvicorn server
# RUN pip install uvicorn[standard]

# # Copy the rest of app
# COPY app app
# COPY alembic alembic
# COPY alembic.ini .
# COPY pyproject.toml .
# COPY init.sh .

# # Create new user to run app process as unprivileged user
# RUN addgroup --gid 1001 --system uvicorn && \
#     adduser --gid 1001 --shell /bin/false --disabled-password --uid 1001 uvicorn

# # Set permissions
# RUN chown -R uvicorn:uvicorn /build

# # Health check
# HEALTHCHECK --interval=30s CMD curl -f http://localhost:8000/ || exit 1

# # Run init.sh script then start uvicorn
# CMD bash init.sh && \
#     runuser -u uvicorn -- /venv/bin/uvicorn app.main:app --app-dir /build --host 0.0.0.0 --port 8000 --workers 2 --loop uvloop

# # Expose the port
# EXPOSE 8000





# Use an official Python runtime as a parent image
FROM python:3.10.4-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create and set the working directory
RUN mkdir /app
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
# Install uvicorn server
RUN pip install uvicorn[standard]

# Copy the rest of app
COPY app app
COPY alembic alembic
COPY alembic.ini .
COPY pyproject.toml .
COPY init.sh .
# Copy the rest of the application code into the container
COPY . /app/

# Expose the port the app runs on
EXPOSE 8000

# Command to run your FastAPI application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
