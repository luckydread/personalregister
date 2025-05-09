# Personal Register API

A FastAPI-based REST API for managing user records with email validation and SQLite database storage.

## Features

- Create single or multiple users with email validation
- Retrieve user information (single user or all users)
- Update user details with email uniqueness validation
- Delete users
- SQLite database with SQLModel ORM
- Input validation using Pydantic models
- Email uniqueness enforcement
- Automatic database creation and table setup

## Prerequisites

- Python 3.10 or higher
- pip (Python package installer)

## Project Structure

```
personalregister/
├── api/
│   └── routes/
│       └── users.py         # User endpoints
├── db/
│   ├── utils/
│   │   └── emailvalidator.py # Email validation utilities
│   └── session.py           # Database session management
├── models/
│   └── models.py           # Data models
├── main.py                 # FastAPI application
├── requirements.txt        # Project dependencies
└── README.md              # This file
```

## Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
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

#### Get User by ID
- **GET** `/users/user/{user_id}`
- Returns a single user by ID

#### Update User
- **PUT** `/users/user/{user_id}`
- Updates user information
- Request body:
  ```json
  {
    "name": "John",
    "surname": "Smith",
    "email": "john.smith@example.com"
  }
  ```

#### Delete User
- **DELETE** `/users/user/{user_id}`
- Deletes a user by ID

### Error Handling

The API returns appropriate HTTP status codes and error messages:

- `400 Bad Request`: Invalid input or duplicate email
- `404 Not Found`: User not found
- `500 Internal Server Error`: Server-side errors

### Interactive Documentation

FastAPI provides automatic interactive API documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Database

The application uses SQLite as the database engine. The database file (`personalregister.db`) is automatically created in the project root directory when the application starts.

## Development

To add new features or modify existing ones:

1. Create a new branch
2. Make your changes
3. Write tests (if applicable)
4. Submit a pull request

## License

[Add your license information here]