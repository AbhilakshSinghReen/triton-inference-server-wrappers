import json

from flask import Response


def create_explicit_model_control_not_allowed_response():
    response_content = {
        "error": "explicit model load / unload is not allowed if polling is enabled",
    }
    
    response_json = json.dumps(response_content)
    
    headers = {
        'Content-Type': 'application/json',
        'Content-Length': str(len(response_json))
    }
    
    response = Response(response=response_json, status=400, headers=headers)
    
    return response


explicit_model_control_not_allowed_response = create_explicit_model_control_not_allowed_response()
