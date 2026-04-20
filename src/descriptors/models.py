from typing import Any, TypeAlias

JSON: TypeAlias = dict[str, Any]


class Model:
    def __init__(self, payload: JSON):
        self.payload = payload


class Field:
    def __init__(self, path: str):
        self.path = path

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self

        keys = self.path.split('.')
        data = instance.payload

        for key in keys:
            if isinstance(data, dict) and key in data:
                data = data[key]
            else:
                return None
        return data

    def __set__(self, instance, value):
        keys = self.path.split('.')
        data = instance.payload

        for key in keys[:-1]:
            data = data[key]

        last_key = keys[-1]
        data[last_key] = value
