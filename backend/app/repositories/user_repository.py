from uuid import UUID

from sqlalchemy.orm import Session

from app.models.user import User


def get_by_mobile(db: Session, mobile: str) -> User | None:
    return (
        db.query(User)
        .filter(User.mobile == mobile)
        .first()
    )


def get_by_id(db: Session, user_id: UUID) -> User | None:
    return (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )


def create(db: Session, user: User) -> User:
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update(db: Session, user: User, data: dict) -> User:
    for key, value in data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)

    return user


def delete(db: Session, user: User) -> None:
    db.delete(user)
    db.commit()