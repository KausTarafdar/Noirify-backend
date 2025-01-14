from fastapi.responses import JSONResponse
from typing import Any, Dict, Union

def success_response(
    data: Any,
    message: str = "Request Successful",
    code: int = 200,
) -> JSONResponse:
    return JSONResponse(
        status_code=code,
        content={
            "status": "Success",
            "data": data,
            "message": message,
            "code": code
        }
    )


def error_response(
    error_type: str,
    details: Union[str, Dict[str, Any]],
    message: str = "An error occurred",
    code: int = 400
) -> JSONResponse:
    return JSONResponse(
        status_code=code,
        content={
            "status": "error",
            "error": {
                "type": error_type,
                "details": details
            },
            "message": message,
            "code": code
        }
    )