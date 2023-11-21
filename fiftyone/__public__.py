"""
FiftyOne's public interface.

| Copyright 2017-2023, Voxel51, Inc.
| `voxel51.com <https://voxel51.com/>`_
|
"""
config = None
annotation_config = None
evaluation_config = None
app_config = None


def reload(hard=False):
    """Reloads the current database connection.

    Args:
        hard (False): whether to reconnect using the current in-memory config
            values (False) or reload configs from environment variables (True)
    """
    global config
    global annotation_config
    global evaluation_config
    global app_config

    import fiftyone.core.config as foc
    import fiftyone.core.odm as foo

    if hard:
        config = foc.load_config()
        annotation_config = foc.load_annotation_config()
        evaluation_config = foc.load_evaluation_config()
        app_config = foc.load_app_config()

    foo.disconnect_db()
    foo.establish_db_conn(config)


reload(hard=True)


from .core.aggregations import (
    Aggregation,
    Bounds,
    Count,
    CountValues,
    Distinct,
    FacetAggregations,
    HistogramValues,
    Mean,
    Quantiles,
    Schema,
    ListSchema,
    Std,
    Sum,
    Values,
)
from .core.collections import SaveContext
from .core.config import AppConfig
from .core.dataset import (
    Dataset,
    list_datasets,
    dataset_exists,
    load_dataset,
    delete_dataset,
    delete_datasets,
    delete_non_persistent_datasets,
    get_default_dataset_name,
    make_unique_dataset_name,
    get_default_dataset_dir,
)
from .core.expressions import (
    ViewField,
    ViewExpression,
    VALUE,
)
from .core.fields import (
    flatten_schema,
    ArrayField,
    BooleanField,
    ClassesField,
    ColorField,
    DateField,
    DateTimeField,
    DictField,
    EmbeddedDocumentField,
    EmbeddedDocumentListField,
    Field,
    FrameNumberField,
    FrameSupportField,
    FloatField,
    GeoPointField,
    GeoLineStringField,
    GeoPolygonField,
    GeoMultiPointField,
    GeoMultiLineStringField,
    GeoMultiPolygonField,
    IntField,
    KeypointsField,
    ListField,
    ObjectIdField,
    PolylinePointsField,
    ReferenceField,
    StringField,
    MaskTargetsField,
    VectorField,
)
from .core.frame import Frame
from .core.groups import Group
from .core.labels import (
    Label,
    Attribute,
    BooleanAttribute,
    CategoricalAttribute,
    NumericAttribute,
    ListAttribute,
    Regression,
    Classification,
    Classifications,
    Detection,
    Detections,
    Polyline,
    Polylines,
    Keypoint,
    Keypoints,
    Segmentation,
    Heatmap,
    TemporalDetection,
    TemporalDetections,
    GeoLocation,
    GeoLocations,
)
from .core.logging import (
    get_logging_level,
    set_logging_level,
)
from .core.metadata import (
    Metadata,
    ImageMetadata,
    VideoMetadata,
)
from .core.models import (
    apply_model,
    compute_embeddings,
    compute_patch_embeddings,
    load_model,
    Model,
    ModelConfig,
    EmbeddingsMixin,
    TorchModelMixin,
    ModelManagerConfig,
    ModelManager,
)
from .core.odm import (
    ColorScheme,
    DatasetAppConfig,
    DynamicEmbeddedDocument,
    EmbeddedDocument,
    KeypointSkeleton,
    SidebarGroupDocument,
)
from .core.plots import (
    plot_confusion_matrix,
    plot_pr_curve,
    plot_pr_curves,
    plot_roc_curve,
    lines,
    scatterplot,
    location_scatterplot,
    Plot,
    ResponsivePlot,
    InteractivePlot,
    ViewPlot,
    ViewGrid,
    CategoricalHistogram,
    NumericalHistogram,
)
from .core.runs import (
    RunConfig,
    Run,
    RunResults,
)
from .core.sample import Sample
from .core.spaces import (
    Space,
    Panel,
)
from .core.stages import (
    Concat,
    Exclude,
    ExcludeBy,
    ExcludeFields,
    ExcludeFrames,
    ExcludeGroups,
    ExcludeLabels,
    Exists,
    FilterField,
    FilterLabels,
    FilterKeypoints,
    Flatten,
    GeoNear,
    GeoWithin,
    GroupBy,
    Limit,
    LimitLabels,
    MapLabels,
    Match,
    MatchFrames,
    MatchLabels,
    MatchTags,
    Mongo,
    Shuffle,
    Select,
    SelectBy,
    SelectFields,
    SelectFrames,
    SelectGroups,
    SelectGroupSlices,
    SelectLabels,
    SetField,
    Skip,
    SortBy,
    SortBySimilarity,
    Take,
    ToPatches,
    ToEvaluationPatches,
    ToClips,
    ToTrajectories,
    ToFrames,
)
from .core.session import (
    close_app,
    launch_app,
    Session,
)
from .core.utils import (
    disable_progress_bars,
    pprint,
    pformat,
    ProgressBar,
)
from .core.view import DatasetView
from .utils.eval.classification import (
    evaluate_classifications,
    ClassificationEvaluationConfig,
    ClassificationResults,
)
from .utils.eval.detection import (
    evaluate_detections,
    DetectionEvaluationConfig,
    DetectionResults,
)
from .utils.eval.regression import (
    evaluate_regressions,
    RegressionEvaluationConfig,
    RegressionResults,
)
from .utils.eval.segmentation import (
    evaluate_segmentations,
    SegmentationEvaluationConfig,
    SegmentationResults,
)
from .utils.quickstart import quickstart
