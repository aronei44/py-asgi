from src.exceptions import ValidationError


class BaseModel:
    def __init__(self, **data):
        annotations = self.__annotations__

        for field, field_type in annotations.items():
            if field not in data:
                raise ValidationError(f"Missing field: {field}")

            value = data[field]

            if not isinstance(value, field_type):
                raise ValidationError(
                    f"Field '{field}' expected {field_type}, got {type(value)}"
                )

            setattr(self, field, value)