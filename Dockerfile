# Use an official Python runtime as the base image
FROM python:3

# Set the working directory in the container
WORKDIR /app

# Copy the entire project into the container
COPY . .

# Install the projects with its dependencies
RUN pip install --no-cache-dir .

# Set the command to run your script as the entrypoint
ENTRYPOINT ["python", "-m", "portable_wisdom.wisdom"]
