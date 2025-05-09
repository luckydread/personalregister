from db.session import SessionDep
from models.models import Users, UserBase
from sqlmodel import select
from typing import List

def check_email_exists(email: str, session: SessionDep, exclude_user_id: int | None = None) -> bool:
    query = select(Users).where(Users.email == email)
    if exclude_user_id:
        query = query.where(Users.id != exclude_user_id)
    existing_user = session.exec(query).first()
    return existing_user is not None

def validate_unique_emails(users_data: list[UserBase]) -> List[str]:
    # Check for duplicate emails within the input list
    emails = [user.email for user in users_data]
    if len(emails) != len(set(emails)):
        duplicates = [email for email in emails if emails.count(email) > 1]
        return [f"Duplicate email in request: {email}" for email in set(duplicates)]
    return []