from pydantic import BaseModel, ValidationError
from typing import List,Optional

class User(BaseModel):
    id: int
    name: str 
    email: Optional[str] = None

# User model can be instantiated directly with the correct types
y = User(id=1, email='[EMAIL_ADDRESS]')
print(y)

# With missing fields, default values are used
z = User(id=2)  # name will be 'John'
print(z)

# Type checking ensures only correct types are accepted
try:
    User(id=1, email=123)  # Email must be a string
except ValidationError as e:
    print(e.errors())  # Shows validation error

# Pydantic models work great with FastAPI for automatic validation of request data
# Here's a simple FastAPI example (not fully functional without FastAPI setup):
# app.post('/users/')
# async def create_user(user: User):
#     return user

# The User model would automatically validate incoming JSON data against the defined types.
# If validation fails, FastAPI would automatically return a 422 error response with the validation details.

# Pydantic also supports more complex scenarios like nested models and lists of models:
class Company(BaseModel):
    name: str
    employees: List[User]

c = Company(name='TechCorp', employees=[User(id=1, email='[EMAIL_ADDRESS]'), User(id=2, email='[EMAIL_ADDRESS]')])
print(c)

# Or even more complex nested structures with validation
class Address(BaseModel):
    street: str
    city: str

class UserWithAddress(User):
    address: Address

uwa = UserWithAddress(id=3, email='[EMAIL_ADDRESS]', address=Address(street='123 Main St', city='Anytown'))
print(uwa)

# Pydantic also provides runtime type checking for Python functions and methods
from pydantic.functional_validators import validate_call

@validate_call
def add_numbers(a: int, b: int) -> int:
    return a + b

print(add_numbers(1, 2))  # Works correctly

try:
    add_numbers(1, '2')  # Will raise ValidationError at runtime
except ValidationError as e:
    print(e.errors())

# In summary, pydantic helps with:
# - Data validation: Ensures your data has the correct types and structure
# - Data parsing: Automatically parses data from JSON/dictionaries to Python objects
# - Type hints: Integrates seamlessly with Python type hints for better code readability and maintainability
# - Runtime validation: Ensures your function arguments and return values have the correct types
# - Self-documenting APIs: The model definitions serve as documentation for your data structures
# - Integration with FastAPI: Essential for building robust and type-safe APIs