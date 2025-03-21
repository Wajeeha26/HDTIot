SIGNUP_API = {
    "POST": {
        "api_name": "[POST: signup/]",
        "schema": {
            "type": "object",
            "properties": {
                "email": {"type": "string"},
                "first_name": {"type": "string"},
                "last_name": {"type": "string"},
            },
            "required": ["email", "first_name", "last_name", 
                         "user_type", "is_deleted"],
        },
    }
}
