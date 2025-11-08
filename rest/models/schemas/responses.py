
from flask import Response, jsonify
from pydantic import BaseModel, Field
from typing import Tuple


class BaseResponse(BaseModel):
    code: int = Field(-1, description="Status Code")
    message: str = Field("Unknown Error!", description="Exception Information")

    @property
    def response(self) -> Tuple[Response, int]:
        return jsonify(self.model_dump()), self.code


class BadRequest(BaseResponse):
    code: int = Field(400, description="Status Code")
    message: str = Field("BadRequest", description="Exception Information")


class NotFound(BaseResponse):
    code: int = Field(404, description="Status Code")
    message: str = Field("Not Found!", description="Exception Information")


class InternalServerError(BaseResponse):
    code: int = Field(500, description="Status Code")
    message: str = Field("Internal Server Error!", description="Exception Information")
