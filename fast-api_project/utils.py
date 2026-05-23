from datetime import datetime
from typing import Any, Dict

def success_response(data: Any, message: str = "Success") -> Dict:
    return {
        "status": "success",
        "message": message,
        "data": data,
        "timestamp": datetime.utcnow().isoformat()
    }

def error_response(message: str, code: int = 400) -> Dict:
    return {
        "status": "error",
        "message": message,
        "code": code,
        "timestamp": datetime.utcnow().isoformat()
    }

def paginate(total: int, skip: int, limit: int) -> Dict:
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "pages": (total + limit - 1) // limit
    }
