# Personal Register API

A FastAPI-based REST API for managing users

## Features

- Create single or multiple users with email validation
- Get all users
- Delete a single user
- SQLite database with SQLModel ORM
- Email uniqueness enforcement
- Automatic database creation and table setup

## Prerequisites

- Python 3.10 or higher
- pip (Python package installer)

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/luckydread/personalregister.git
   cd personalregister
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

The API will be available at `http://localhost:8000`

## API Documentation

### Endpoints

#### Create Users
- **POST** `/users/user`
- Creates one or more users
- Request body:
  ```json
  [
    {
      "name": "John",
      "surname": "Doe",
      "email": "john@example.com"
    },
    {
      "name": "Jane",
      "surname": "Doe",
      "email": "jane@example.com"
    }
  ]
  ```
- Response:
  ```json
  {
    "message": "Successfully created 2 users",
    "users": [
      {
        "id": 1,
        "name": "John",
        "surname": "Doe",
        "email": "john@example.com"
      },
      {
        "id": 2,
        "name": "Jane",
        "surname": "Doe",
        "email": "jane@example.com"
      }
    ]
  }
  ```

#### Get All Users
- **GET** `/users/users`
- Returns a list of all users

#### Delete User
- **DELETE** `/users/user/{user_id}`
- Deletes a user by ID

## Database

The application uses SQLite as the database engine. The database file (`personalregister.db`) is automatically created in the project root directory when the application starts.

## Tests

- The test folder contains the following tests:

1. test_root - Tests the root endpoint
2. test_add_users_success - Tests adding a single user
3. test_add_two_users_successfully - Tests adding two users at the same time
4. test_add_users_duplicate_email - Tests that we can't add a user with a duplicate email
5. test_get_users - Tests getting all users
6. test_delete_user - Tests deleting a user
