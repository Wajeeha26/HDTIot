SIGNUP_API = {
    "POST": {
        "api_name": "[POST: signup/]",
        "schema": {
            "type": "object",
            "properties": {
                "uid": {"type": "string"},
                "email": {"type": "string"},
                "first_name": {"type": "string"},
                "last_name": {"type": "string"},
                "user_type": {"type": "integer", "default": 1},
                "is_deleted": {"type": "integer", "default": 0},
            },
            "required": ["uid", "email", "first_name", "last_name"],
        },
    }
}
