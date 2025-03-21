USER_API = {
    "GET": {
        "api_name": "[GET: user/]",
        "schema": {
            "type": "object",
            "properties": {
                "uid": {"type": "string"},
            },
            "required": ["uid"],
        },
    },
    "PUT": {
        "api_name": "[PUT: user/]",
        "schema": {
            "type": "object",
            "properties": {
                "email": {"type": "string", "format": "email"},
                "first_name": {"type": "string", "minLength": 2,
                                "maxLength": 50},
                "last_name": {"type": "string", "minLength": 2,
                               "maxLength": 50},
            },
            "required": [],
        },
    },
    "DELETE": {
        "api_name": "[DELETE: user/]",
        "schema": {
            "type": "object",
            "properties": {
                "uid": {"type": "string"},
            },
            "required": ["uid"],
        },
    },
}
