"""
FiftyOne Server state

| Copyright 2017-2022, Voxel51, Inc.
| `voxel51.com <https://voxel51.com/>`_
|
"""
import typing as t

import asyncio
from starlette.requests import Request
from starlette.websockets import WebSocket

import fiftyone.core.state as fos


_listeners: t.Dict[
    t.Union[Request, WebSocket], asyncio.Queue[fos.StateDescription]
] = {}
_state = fos.StateDescription()


def get_state() -> fos.StateDescription:
    return _state


def set_state(
    state: fos.StateDescription, source: t.Union[Request, WebSocket] = None
) -> None:
    global _state
    _state = state

    events = []
    for listener, queue_or_callback in _listeners.items():
        if source is listener:
            continue

        if isinstance(queue_or_callback, asyncio.LifoQueue):
            event = queue_or_callback.put(state)
        else:
            event = queue_or_callback()

        events.append(event)

    asyncio.gather(*events)


async def subscribe(
    websocket: WebSocket, callback: t.Callable[[], None]
) -> t.Callable[[], None]:
    _listeners[websocket] = callback

    def cleanup():
        _listeners.pop(websocket)

    return cleanup


async def listen(request: Request,) -> t.AsyncIterator[fos.StateDescription]:
    def cleanup() -> None:
        _listeners.pop(request)

    _listeners[request] = asyncio.LifoQueue(maxsize=1)

    try:
        yield get_state()
        while True:
            state = await _listeners[request].get()
            disconnected = await request.is_disconnected

            if disconnected:
                cleanup()
                break

            yield state

    except asyncio.CancelledError as e:
        cleanup()
        raise e
