login_schema = {
    "username": {"type": "string", "maxlength": 255, "required": True},
    "password": {"type": "string", "minlength": 8, "maxlength": 255, "required": True},
    "pin": {"type": "integer", "required": True},
}

register_schema = {
    "username": {"type": "string", "maxlength": 255, "required": True},
    "password": {"type": "string", "minlength": 8, "maxlength": 255, "required": True},
    "pin": {"type": "integer", "required": True},
    "name": {"type": "string", "maxlength": 255, "required": True},
    "email": {
        "type": "string",
        "regex": r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
        "maxlength": 255,
        "required": True,
    },
    "city_name": {"type": "string", "maxlength": 255, "required": True},
    "address": {"type": "string", "maxlength": 255, "required": True},
}

update_profile_schema = {
    "username": {"type": "string", "maxlength": 255, "required": False},
    "password": {"type": "string", "minlength": 8, "maxlength": 255, "required": False},
    "pin": {"type": "integer", "required": False},
    "name": {"type": "string", "maxlength": 255, "required": False},
    "email": {
        "type": "string",
        "regex": r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
        "maxlength": 255,
        "required": False,
    },
    "city_name": {"type": "string", "maxlength": 255, "required": False},
    "address": {"type": "string", "maxlength": 255, "required": False},
}
