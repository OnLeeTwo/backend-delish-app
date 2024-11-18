create_review_schema = {
    "restaurant_id": {"type": "integer", "required": True},
    "score": {"type": "integer", "min": 0, "max": 5, "nullable": True},
    "review_body": {"type": "string", "nullable": True},
    "review_status": {"type": "string", "nullable": True},
}

submit_review_schema = {
    "review": {
        "type": "dict",
        "schema": {
            "score": {"type": "integer", "min": 0, "max": 5},
            "review_body": {"type": "string"},
            "review_status": {"type": "string"},
        },
    },
    "food": {
        "type": "dict",
        "schema": {
            "food_score": {"type": "integer", "min": 0, "max": 5},
            "food_comment": {"type": "string", "nullable": True},
        },
    },
    "service": {
        "type": "dict",
        "schema": {
            "service_score": {"type": "integer", "min": 0, "max": 5},
            "service_comment": {"type": "string", "nullable": True},
        },
    },
    "ambience": {
        "type": "dict",
        "schema": {
            "ambience_score": {"type": "integer", "min": 0, "max": 5},
            "ambience_comment": {"type": "string", "nullable": True},
        },
    },
    "media": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {"location": {"type": "string", "nullable": True}},
        },
    },
}
