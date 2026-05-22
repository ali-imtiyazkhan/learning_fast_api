from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    id: int
    name: str
    email: str
    age: Optional[int] = None

# ✅ Valid — "42" is coerced to int automatically
user = User(id="42", name="Alice", email="alice@example.com")
print(user.id)    # → 42 (int, not str)
print(user.age)   # → None

# ❌ Invalid — raises ValidationError
User(id="not-a-number", name="Bob", email="b@b.com")