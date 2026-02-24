from src.depends import Depends


def get_db():
    print("connect db")
    return "db result"

def get_user(db=Depends(get_db)):
    return f"user result({db})"

def get_profile(user=Depends(get_user)):
    return f"profile result({user})"