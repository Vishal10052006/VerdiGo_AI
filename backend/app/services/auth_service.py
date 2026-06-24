from app.models.user import User


def create_user(db, data):
    user = User(
        mobile=data.mobile,
        email=data.email,
        login_type=data.login_type
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user