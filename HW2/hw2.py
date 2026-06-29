from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator
import json

class Address(BaseModel):
    city: str = Field(..., min_length=2)
    street: str = Field(..., min_length=3)
    house_number: int = Field(..., gt=0)

class User(BaseModel):
    name: str = Field(..., min_length=2)
    age: int = Field(..., ge=0, le=120)
    email: EmailStr
    is_employed: bool
    address: Address

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        if not all(part.isalpha() for part in value.split()):
            raise ValueError("Name must contain only letters.")
        return value

    @model_validator(mode="after")
    def validate_employment_age(self):
        if self.is_employed and not (18 <= self.age <= 65):
            raise ValueError(
                "An employed user must be between 18 and 65 years old."
            )
        return self

def register_user(json_input: str) -> str:
    """
    Принимает JSON-строку, валидирует данные и возвращает сериализованный JSON.
    """
    data = json.loads(json_input)

    user = User.model_validate(data)

    return user.model_dump_json(indent=4)

json_input = """
{
    "name": "John Doe",
    "age": 30,
    "email": "john.doe@example.com",
    "is_employed": true,
    "address": {
        "city": "New York",
        "street": "5th Avenue",
        "house_number": 123
    }
}
"""
try:
    print(register_user(json_input))
except Exception as e:
    print(e)