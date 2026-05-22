from pydantic import BaseModel, Field, EmailStr

class Product(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    price: float = Field(gt=0, description="Must be positive")
    stock: int = Field(ge=0, default=0)
    sku: str = Field(pattern=r"^[A-Z]{3}-\d{4}$")

# ✅ Valid
Product(name="Widget", price=9.99, sku="WDG-1234")

# ❌ price must be > 0
Product(name="Widget", price=-5, sku="WDG-1234")

# ❌ sku pattern mismatch
Product(name="Widget", price=10, sku="widget-1")