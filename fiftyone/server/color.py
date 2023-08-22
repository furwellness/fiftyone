"""
FiftyOne Server coloring

| Copyright 2017-2023, Voxel51, Inc.
| `voxel51.com <https://voxel51.com/>`_
|
"""
from dataclasses import asdict
import typing as t

from bson import ObjectId
import strawberry as gql

import fiftyone as fo
import fiftyone.core.session.events as fose
import fiftyone.core.odm as foo
import fiftyone.core.utils as fou

from fiftyone.server.events import dispatch_event, get_state


@gql.type
class ValueColor:
    color: str
    value: str


@gql.type
class CustomizeColor:
    path: str
    valueColors: t.Optional[t.List[ValueColor]] = None
    colorByAttribute: t.Optional[str] = None
    fieldColor: t.Optional[str] = None


@gql.type
class ColorScheme:
    id: gql.ID = gql.field(default_factory=lambda: str(ObjectId()))
    color_pool: t.List[str]
    fields: t.Optional[t.List[CustomizeColor]] = None


@gql.input
class ValueColorInput:
    color: str
    value: str


@gql.input
class CustomizeColorInput:
    path: str
    valueColors: t.Optional[t.List[ValueColorInput]] = None
    colorByAttribute: t.Optional[str] = None
    fieldColor: t.Optional[str] = None


@gql.input
class ColorSchemeInput:
    color_pool: t.List[str]
    fields: t.List[CustomizeColorInput]


@gql.type
class SetColorScheme:
    @gql.field
    async def set_color_scheme(
        self,
        subscription: str,
        color_scheme: ColorSchemeInput,
    ) -> bool:
        state = get_state()
        state.color_scheme = _to_odm_color_scheme(color_scheme)

        await dispatch_event(
            subscription, fose.SetColorScheme(color_scheme=color_scheme)
        )
        return True

    @gql.field
    async def set_dataset_color_scheme(
        self,
        dataset_name: str,
        color_scheme: t.Optional[ColorSchemeInput] = None,
    ) -> None:
        def run():
            dataset = fo.load_dataset(dataset_name)
            dataset.app_config.color_scheme = (
                foo.ColorScheme(
                    color_pool=color_scheme.color_pool,
                    fields=[asdict(f) for f in color_scheme.fields]
                    if color_scheme.fields
                    else None,
                )
                if color_scheme
                else None
            )
            dataset.save()

        await fou.run_sync_task(run)


def _to_odm_color_scheme(color_scheme: ColorSchemeInput):
    return foo.ColorScheme(
        color_pool=color_scheme.color_pool,
        fields=[asdict(f) for f in color_scheme.fields]
        if color_scheme.fields
        else [],
    )
