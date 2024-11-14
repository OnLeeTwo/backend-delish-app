login_email_schema = {
    "email": {"type": "string", "maxlength": 255, "required": True},
    "password": {"type": "string", "minlength": 8, "maxlength": 255, "required": True},
}

login_phone_schema = {
    "phone_number": {"type": "string", "maxlength": 255, "required": True},
    "pin": {"type": "string", "minlength": 4, "maxlength": 255, "required": True},
}

register_schema = {
    "username": {"type": "string", "maxlength": 255, "required": True},
    "password": {"type": "string", "minlength": 8, "maxlength": 255, "required": True},
    "pin": {"type": "string", "minlength": 4, "maxlength": 255, "required": True},
    "name": {"type": "string", "maxlength": 255, "required": True},
    "email": {
        "type": "string",
        "regex": r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
        "maxlength": 255,
        "required": True,
    },
    "city_name": {"type": "string", "maxlength": 255, "required": True},
    "address": {"type": "string", "maxlength": 255, "required": True},
    "phone_number": {"type": "string", "maxlength": 255, "required": True},
}

update_profile_schema = {
    "username": {"type": "string", "maxlength": 255, "required": False},
    "password": {"type": "string", "minlength": 8, "maxlength": 255, "required": False},
    "pin": {"type": "string", "minlength": 4, "maxlength": 255, "required": False},
    "name": {"type": "string", "maxlength": 255, "required": False},
    "email": {
        "type": "string",
        "regex": r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
        "maxlength": 255,
        "required": False,
    },
    "city_name": {"type": "string", "maxlength": 255, "required": False},
    "address": {"type": "string", "maxlength": 255, "required": False},
    "phone_number": {"type": "string", "maxlength": 255, "required": False},
}
