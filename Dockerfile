FROM python:3.9


# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Set the working directory to /app
WORKDIR /app

# Create a virtual environment and activate it
RUN python -m venv venv
ENV PATH="/venv/bin:$PATH"

# Activate the virtual environment
RUN . venv/bin/activate

# Copy the requirements file into the container at /app
COPY requirements.txt .
COPY .env.example /app/.env

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Expose port 8000 to the outside world
EXPOSE 8000

# Run the Django development server
CMD ["python", "manage.py", "runserver"]