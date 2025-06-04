from pydantic import BaseModel


class LoginModel(BaseModel):
    username: str
    password: str
    message: str
    submit: str


class ProductBasicModel(BaseModel):
    productname: str
