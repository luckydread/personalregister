from fastapi import APIRouter, HTTPException
from models.models import Users, UserBase, UserResponse, UsersResponse
from db.session import SessionDep
from sqlmodel import select
from db.utils.emailvalidator import check_email_exists, validate_unique_emails
from typing import List
from pydantic import BaseModel

class UsersResponse(BaseModel):
    message: str
    users: List[Users]

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/user", response_model=UsersResponse)
def add_users(users_data: list[UserBase], session: SessionDep) -> UsersResponse:
    # First validate for duplicate emails in the request
    duplicate_errors = validate_unique_emails(users_data)
    if duplicate_errors:
        raise HTTPException(
            status_code=400,
            detail={"message": "Validation error", "errors": duplicate_errors}
        )
    
    # Check for existing emails in database
    existing_emails = []
    for user_data in users_data:
        if check_email_exists(user_data.email, session):
            existing_emails.append(user_data.email)
    
    if existing_emails:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Email already exists",
                "errors": [f"Email already exists: {email}" for email in existing_emails]
            }
        )
    
    # Create all users in a transaction
    created_users = []
    try:
        for user_data in users_data:
            user = Users.from_orm(user_data)
            session.add(user)
            created_users.append(user)
        
        session.commit()
        # Refresh all users to get their IDs
        for user in created_users:
            session.refresh(user)
            
        return UsersResponse(
            message=f"Successfully created {len(created_users)} users",
            users=created_users
        )
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error creating users: {str(e)}"
        )

# Get all users
@router.get("/users", response_model=List[UserResponse])
def get_users(session: SessionDep) -> List[UserResponse]:
    users = session.exec(select(Users)).all()
    return users

# Delete a user
@router.delete("/user/{user_id}")
def delete_user(user_id: int, session: SessionDep) -> dict:
    user = session.get(Users, user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    
    session.delete(user)
    session.commit()
    return {"message": f"User {user.email} deleted successfully"}
