"""
FiftyOne Server decorators.

| Copyright 2017-2022, Voxel51, Inc.
| `voxel51.com <https://voxel51.com/>`_
|
"""
import traceback
import typing as t

from starlette.endpoints import HTTPEndpoint
from starlette.responses import Response
from starlette.requests import Request

from fiftyone.server.json_util import FiftyOneJSONEncoder, FiftyOneResponse


def route(func):
    async def wrapper(
        endpoint: HTTPEndpoint, request: Request, *args
    ) -> t.Union[dict, Response]:
        try:
            body = await request.body()
            payload = body.decode("utf-8")
            data = FiftyOneJSONEncoder.loads(payload) if payload else {}
            response = await func(endpoint, request, data, *args)
            if isinstance(response, Response):
                return response

            return FiftyOneResponse(response)
        except:
            return FiftyOneResponse(
                {"kind": "Server Error", "stack": traceback.format_exc(),}
            )

    return wrapper
