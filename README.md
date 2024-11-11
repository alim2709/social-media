# Social Media App

This project is a social media web application built with **FastAPI** for the backend, **PostgreSQL** as the database, and **Docker** for containerization. It leverages **SQLAlchemy** for ORM (Object-Relational Mapping) to manage database interactions and **Pydantic** for data validation and serialization.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Environment Setup](#environment-setup)
- [Running the Project](#running-the-project)
- [Running Tests](#running-tests)

## Features
- **User Authentication**: Secure registration and login functionality.
- **Post Publishing**: Users can create, edit, and delete posts.
- **Post Comments**: Users can comment on posts, with support for nested replies.
- **Auto-Reply**: Automatic reply feature for comments, powered by a generative AI model to provide thoughtful responses based on the content of the post and comment.


## Requirements

- Docker and Docker Compose
- Python 3.10

## Environment Setup

1. **Clone the repository:**

   ```
   git clone https://github.com/alim2709/social-media.git
   cd social-media-app

2.   **Environment Variables**

    To configure environment variables, this project includes an `env.sample` file as a template. This file lists all required environment variables with example values. You can use it to create your own `.env` file with the actual values for your environment.
    
3. **Edit the .env file and update the values as needed:**

    ```
    DB_PASS=YOUR_DB_PASS
    TEST_DB_PASS=YOUR_DB_PASS
    POSTGRES_PASSWORD=YOUR_DB_PASS
    TEST_POSTGRES_PASSWORD=YOUR_DB_PASS
    JWT_SECRET_KEY=JWT_SECRET_KEY
    ACCESS_TOKEN_EXPIRE_MINUTES=ACCESS_TOKEN_EXPIRE_MINUTES
    REFRESH_TOKEN_EXPIRE_DAYS=REFRESH_TOKEN_EXPIRE_DAYS
    GOOGLE_AI_SECRET_KEY=YOUR_GOOGLE_AI_SECRET_KEY
   ```
   To generate GOOGLE_AI_SECRET_KEY visit this link https://ai.google.dev/pricing#1_5flash


## Running the project

1. **Start Docker containers:**
    ```
   docker compose up --build
   ```
2. **Check container status:**
    ```
   docker compose ps 
    ```
3. **Two options:**
- **Option 1 Run migrations:**
   ```
   docker compose exec social-media-app alembic upgrade head
   ```
- **Option 2 Run db_backup file:**

  Copy the dump file:
     ```
     docker cp ./data/db_backup.sql db:/tmp/db_backup.sql
     ```
   
  Run the restore command:
     ```
     docker exec -i db psql -U postgres -d db -f /tmp/db_backup.sql
     ```

  Testing APIs with test_user:
  ```
  email: test@test.com
  password: testtesttest
  ```
  
4. **Access the application:**
   
   The app should now be available at http://localhost:7777.


## Running tests

1. **Prepare test database:**
   
   ##### Run this command 
   ```
   docker exec -it db psql -U postgres -c "CREATE DATABASE db_test;"
   ```
2. **Run tests**

   ```
   docker exec -it social-media-app pytest -v
   ```