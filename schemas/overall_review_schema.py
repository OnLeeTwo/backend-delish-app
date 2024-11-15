create_review_schema = {
    "score": {
        "type": "int",
        "required": True,
    },
    "review_status": {
        "type": "string",
        "maxlength": 255,
        "required": True,
    },
    "review_body": {
        "type": "string",
        "required": False,
    }
}