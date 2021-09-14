from pydantic import BaseModel


class BaseEnumConfig(BaseModel):
    class Config:
        use_enum_values = True

