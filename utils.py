from typing import Any, Dict


def response(code: int, message: str, data: Any = None) -> Dict[str, Any]:
    return {
        'code': code,
        'message': message,
        'data': data
    }
