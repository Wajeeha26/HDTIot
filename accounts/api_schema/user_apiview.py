USER_API = {
    "GET": {
        "api_name": "[GET: user/]",
        "schema": {
            "type": "object",
            "properties": {
                "uid": {"type": "string"},
            },
            "required": ["uid"],
        }
    },
    "PUT": {
        "api_name": "[PUT: user/]",
        "schema": {
            "type": "object",
            "properties": {
                "uid": {"type": "string"},
            },
            "required": ["uid"],
        }
    },
    "DELETE": {
        "api_name": "[DELETE: user/]",
        "schema": {
            "type": "object",
            "properties": {
                "uid": {"type": "string"},
            },
            "required": ["uid"],
        }
    }
}
