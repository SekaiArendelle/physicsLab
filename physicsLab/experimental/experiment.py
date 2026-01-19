# -*- coding: utf-8 -*-

import json
from typing import Optional, List, Dict, Any, TypedDict


# StatusSave JSON structure types
class ElementProperties(TypedDict, total=False):
    high_level: float
    low_level: float
    max_current: float
    rated_voltage: float
    rated_power: float
    locked: float
    ac_voltage: float
    dc_voltage: float
    frequency: float
    switch: float


class ElementStatistics(TypedDict, total=False):
    current: float
    voltage: float
    power: float
    state: float
    input0: float
    output0: float
    temperature: float
    resistance: float
    instantaneous_power: float
    instantaneous_voltage: float
    instantaneous_current: float
    instantaneous_resistance: float


class ElementPosition(TypedDict):
    x: float
    y: float
    magnitude: float


class Wire(TypedDict):
    source: str
    source_pin: int
    target: str
    target_pin: int
    color_name: str


class CircuitElement(TypedDict):
    model_id: str
    identifier: str
    label: Optional[str]
    is_broken: bool
    is_locked: bool
    properties: ElementProperties
    statistics: ElementStatistics
    position: str  # Format: "x,y,z"
    rotation: str  # Format: "x,y,z"
    diagram_cached: bool
    diagram_position: ElementPosition
    diagram_rotation: float


class StatusSaveData(TypedDict, total=False):
    simulation_speed: float
    elements: List[CircuitElement]
    wires: List[Wire]


class CameraPosition(TypedDict):
    mode: int
    distance: float
    vision_center: str  # Format: "x,y,z"
    target_rotation: str  # Format: "x,y,z"


# StatusSave and CameraSave are JSON strings containing the above structures
StatusSave = str  # JSON string of StatusSaveData
CameraSave = str  # JSON string of CameraPosition


def parse_status_save(status_save_json: StatusSave) -> StatusSaveData:
    """Parse StatusSave JSON string into structured data."""
    return json.loads(status_save_json)


def serialize_status_save(status_data: StatusSaveData) -> StatusSave:
    """Serialize StatusSave data into JSON string."""
    return json.dumps(status_data)


def parse_camera_save(camera_save_json: CameraSave) -> CameraPosition:
    """Parse CameraSave JSON string into structured data."""
    return json.loads(camera_save_json)


def serialize_camera_save(camera_data: CameraPosition) -> CameraSave:
    """Serialize CameraSave data into JSON string."""
    return json.dumps(camera_data)


class ExperimentInfo:
    """Experiment metadata information."""

    id: Optional[str]
    type: int
    components: int
    subject: Optional[str]
    status_save: Optional[StatusSave]
    camera_save: Optional[CameraSave]
    version: int
    creation_date: int
    paused: bool
    summary: Optional[Any]
    plots: Optional[Any]

    def __init__(
        self,
        experiment_id: Optional[str] = None,
        experiment_type: int = 0,
        components: int = 0,
        subject: Optional[str] = None,
        status_save: Optional[StatusSave] = None,
        camera_save: Optional[CameraSave] = None,
        version: int = 2404,
        creation_date: int = 0,
        paused: bool = False,
        summary: Optional[Any] = None,
        plots: Optional[Any] = None,
    ) -> None:
        if not isinstance(experiment_id, (str, type(None))):
            raise TypeError(
                f"Parameter `experiment_id` must be of type `str` or None, but got value `{experiment_id}` of type `{type(experiment_id).__name__}`"
            )
        self.id = experiment_id
        if not isinstance(experiment_type, int):
            raise TypeError(
                f"Parameter `experiment_type` must be of type `int`, but got value `{experiment_type}` of type `{type(experiment_type).__name__}`"
            )
        self.type = experiment_type
        if not isinstance(components, int):
            raise TypeError(
                f"Parameter `components` must be of type `int`, but got value `{components}` of type `{type(components).__name__}`"
            )
        self.components = components
        if not isinstance(subject, (str, type(None))):
            raise TypeError(
                f"Parameter `subject` must be of type `str` or None, but got value `{subject}` of type `{type(subject).__name__}`"
            )
        self.subject = subject
        if not isinstance(status_save, (str, type(None))):
            raise TypeError(
                f"Parameter `status_save` must be of type `StatusSave` or None, but got value `{status_save}` of type `{type(status_save).__name__}`"
            )
        self.status_save = status_save
        if not isinstance(camera_save, (str, type(None))):
            raise TypeError(
                f"Parameter `camera_save` must be of type `CameraSave` or None, but got value `{camera_save}` of type `{type(camera_save).__name__}`"
            )
        self.camera_save = camera_save
        if not isinstance(version, int):
            raise TypeError(
                f"Parameter `version` must be of type `int`, but got value `{version}` of type `{type(version).__name__}`"
            )
        self.version = version
        if not isinstance(creation_date, int):
            raise TypeError(
                f"Parameter `creation_date` must be of type `int`, but got value `{creation_date}` of type `{type(creation_date).__name__}`"
            )
        self.creation_date = creation_date
        if not isinstance(paused, bool):
            raise TypeError(
                f"Parameter `paused` must be of type `bool`, but got value `{paused}` of type `{type(paused).__name__}`"
            )
        self.paused = paused
        self.summary = summary
        self.plots = plots


class UserInfo:
    """User information embedded in experiment summary."""

    id: Optional[str]
    nickname: Optional[str]
    signature: Optional[str]
    avatar: int
    avatar_region: int
    decoration: int
    verification: Optional[str]

    def __init__(
        self,
        user_id: Optional[str] = None,
        nickname: Optional[str] = None,
        signature: Optional[str] = None,
        avatar: int = 0,
        avatar_region: int = 0,
        decoration: int = 0,
        verification: Optional[str] = None,
    ) -> None:
        if not isinstance(user_id, (str, type(None))):
            raise TypeError(
                f"Parameter `user_id` must be of type `str` or None, but got value `{user_id}` of type `{type(user_id).__name__}`"
            )
        self.id = user_id
        if not isinstance(nickname, (str, type(None))):
            raise TypeError(
                f"Parameter `nickname` must be of type `str` or None, but got value `{nickname}` of type `{type(nickname).__name__}`"
            )
        self.nickname = nickname
        if not isinstance(signature, (str, type(None))):
            raise TypeError(
                f"Parameter `signature` must be of type `str` or None, but got value `{signature}` of type `{type(signature).__name__}`"
            )
        self.signature = signature
        if not isinstance(avatar, int):
            raise TypeError(
                f"Parameter `avatar` must be of type `int`, but got value `{avatar}` of type `{type(avatar).__name__}`"
            )
        self.avatar = avatar
        if not isinstance(avatar_region, int):
            raise TypeError(
                f"Parameter `avatar_region` must be of type `int`, but got value `{avatar_region}` of type `{type(avatar_region).__name__}`"
            )
        self.avatar_region = avatar_region
        if not isinstance(decoration, int):
            raise TypeError(
                f"Parameter `decoration` must be of type `int`, but got value `{decoration}` of type `{type(decoration).__name__}`"
            )
        self.decoration = decoration
        if not isinstance(verification, (str, type(None))):
            raise TypeError(
                f"Parameter `verification` must be of type `str` or None, but got value `{verification}` of type `{type(verification).__name__}`"
            )
        self.verification = verification


class Summary:
    """Experiment summary information for publication."""

    type: int
    parent_id: Optional[str]
    parent_name: Optional[str]
    parent_category: Optional[str]
    content_id: Optional[str]
    editor: Optional[str]
    coauthors: List[str]
    description: Optional[str]
    localized_description: Optional[str]
    tags: List[str]
    model_id: Optional[str]
    model_name: Optional[str]
    model_tags: List[str]
    version: int
    language: Optional[str]
    visits: int
    stars: int
    supports: int
    remixes: int
    comments: int
    price: int
    popularity: int
    creation_date: Any
    update_date: int
    sorting_date: int
    id: Optional[str]
    category: Optional[str]
    subject: Optional[str]
    localized_subject: Optional[str]
    image: int
    image_region: int
    user: UserInfo
    visibility: int
    settings: Dict[str, Any]
    anonymous: bool
    multilingual: bool

    def __init__(
        self,
        summary_type: int = 0,
        parent_id: Optional[str] = None,
        parent_name: Optional[str] = None,
        parent_category: Optional[str] = None,
        content_id: Optional[str] = None,
        editor: Optional[str] = None,
        coauthors: Optional[List[str]] = None,
        description: Optional[str] = None,
        localized_description: Optional[str] = None,
        tags: Optional[List[str]] = None,
        model_id: Optional[str] = None,
        model_name: Optional[str] = None,
        model_tags: Optional[List[str]] = None,
        version: int = 0,
        language: Optional[str] = "Chinese",
        visits: int = 0,
        stars: int = 0,
        supports: int = 0,
        remixes: int = 0,
        comments: int = 0,
        price: int = 0,
        popularity: int = 0,
        creation_date: int = 0,
        update_date: int = 0,
        sorting_date: int = 0,
        summary_id: Optional[str] = None,
        category: Optional[str] = None,
        subject: Optional[str] = None,
        localized_subject: Optional[str] = None,
        image: int = 0,
        image_region: int = 0,
        user: Optional[UserInfo] = None,
        visibility: int = 0,
        settings: Optional[Dict[str, Any]] = None,
        anonymous: bool = False,
        multilingual: bool = False,
    ) -> None:
        if not isinstance(summary_type, int):
            raise TypeError(
                f"Parameter `summary_type` must be of type `int`, but got value `{summary_type}` of type `{type(summary_type).__name__}`"
            )
        self.type = summary_type
        if not isinstance(parent_id, (str, type(None))):
            raise TypeError(
                f"Parameter `parent_id` must be of type `str` or None, but got value `{parent_id}` of type `{type(parent_id).__name__}`"
            )
        self.parent_id = parent_id
        if not isinstance(parent_name, (str, type(None))):
            raise TypeError(
                f"Parameter `parent_name` must be of type `str` or None, but got value `{parent_name}` of type `{type(parent_name).__name__}`"
            )
        self.parent_name = parent_name
        if not isinstance(parent_category, (str, type(None))):
            raise TypeError(
                f"Parameter `parent_category` must be of type `str` or None, but got value `{parent_category}` of type `{type(parent_category).__name__}`"
            )
        self.parent_category = parent_category
        if not isinstance(content_id, (str, type(None))):
            raise TypeError(
                f"Parameter `content_id` must be of type `str` or None, but got value `{content_id}` of type `{type(content_id).__name__}`"
            )
        self.content_id = content_id
        if not isinstance(editor, (str, type(None))):
            raise TypeError(
                f"Parameter `editor` must be of type `str` or None, but got value `{editor}` of type `{type(editor).__name__}`"
            )
        self.editor = editor

        if not isinstance(coauthors, (list, type(None))):
            raise TypeError(
                f"Parameter `coauthors` must be of type `list` or None, but got value `{coauthors}` of type `{type(coauthors).__name__}`"
            )
        self.coauthors = coauthors if coauthors is not None else []

        if not isinstance(description, (str, type(None))):
            raise TypeError(
                f"Parameter `description` must be of type `str` or None, but got value `{description}` of type `{type(description).__name__}`"
            )
        self.description = description
        if not isinstance(localized_description, (str, type(None))):
            raise TypeError(
                f"Parameter `localized_description` must be of type `str` or None, but got value `{localized_description}` of type `{type(localized_description).__name__}`"
            )
        self.localized_description = localized_description

        if not isinstance(tags, (list, type(None))):
            raise TypeError(
                f"Parameter `tags` must be of type `list` or None, but got value `{tags}` of type `{type(tags).__name__}`"
            )
        self.tags = tags if tags is not None else [f"Type-{summary_type}"]

        if not isinstance(model_id, (str, type(None))):
            raise TypeError(
                f"Parameter `model_id` must be of type `str` or None, but got value `{model_id}` of type `{type(model_id).__name__}`"
            )
        self.model_id = model_id
        if not isinstance(model_name, (str, type(None))):
            raise TypeError(
                f"Parameter `model_name` must be of type `str` or None, but got value `{model_name}` of type `{type(model_name).__name__}`"
            )
        self.model_name = model_name

        if not isinstance(model_tags, (list, type(None))):
            raise TypeError(
                f"Parameter `model_tags` must be of type `list` or None, but got value `{model_tags}` of type `{type(model_tags).__name__}`"
            )
        self.model_tags = model_tags if model_tags is not None else []

        if not isinstance(version, int):
            raise TypeError(
                f"Parameter `version` must be of type `int`, but got value `{version}` of type `{type(version).__name__}`"
            )
        self.version = version
        if not isinstance(language, (str, type(None))):
            raise TypeError(
                f"Parameter `language` must be of type `str` or None, but got value `{language}` of type `{type(language).__name__}`"
            )
        self.language = language
        if not isinstance(visits, int):
            raise TypeError(
                f"Parameter `visits` must be of type `int`, but got value `{visits}` of type `{type(visits).__name__}`"
            )
        self.visits = visits
        if not isinstance(stars, int):
            raise TypeError(
                f"Parameter `stars` must be of type `int`, but got value `{stars}` of type `{type(stars).__name__}`"
            )
        self.stars = stars
        if not isinstance(supports, int):
            raise TypeError(
                f"Parameter `supports` must be of type `int`, but got value `{supports}` of type `{type(supports).__name__}`"
            )
        self.supports = supports
        if not isinstance(remixes, int):
            raise TypeError(
                f"Parameter `remixes` must be of type `int`, but got value `{remixes}` of type `{type(remixes).__name__}`"
            )
        self.remixes = remixes
        if not isinstance(comments, int):
            raise TypeError(
                f"Parameter `comments` must be of type `int`, but got value `{comments}` of type `{type(comments).__name__}`"
            )
        self.comments = comments
        if not isinstance(price, int):
            raise TypeError(
                f"Parameter `price` must be of type `int`, but got value `{price}` of type `{type(price).__name__}`"
            )
        self.price = price
        if not isinstance(popularity, int):
            raise TypeError(
                f"Parameter `popularity` must be of type `int`, but got value `{popularity}` of type `{type(popularity).__name__}`"
            )
        self.popularity = popularity
        if not isinstance(creation_date, int):
            raise TypeError(
                f"Parameter `creation_date` must be of type `int`, but got value `{creation_date}` of type `{type(creation_date).__name__}`"
            )
        self.creation_date = creation_date
        if not isinstance(update_date, int):
            raise TypeError(
                f"Parameter `update_date` must be of type `int`, but got value `{update_date}` of type `{type(update_date).__name__}`"
            )
        self.update_date = update_date
        if not isinstance(sorting_date, int):
            raise TypeError(
                f"Parameter `sorting_date` must be of type `int`, but got value `{sorting_date}` of type `{type(sorting_date).__name__}`"
            )
        self.sorting_date = sorting_date
        if not isinstance(summary_id, (str, type(None))):
            raise TypeError(
                f"Parameter `summary_id` must be of type `str` or None, but got value `{summary_id}` of type `{type(summary_id).__name__}`"
            )
        self.id = summary_id
        if not isinstance(category, (str, type(None))):
            raise TypeError(
                f"Parameter `category` must be of type `str` or None, but got value `{category}` of type `{type(category).__name__}`"
            )
        self.category = category
        if not isinstance(subject, (str, type(None))):
            raise TypeError(
                f"Parameter `subject` must be of type `str` or None, but got value `{subject}` of type `{type(subject).__name__}`"
            )
        self.subject = subject
        if not isinstance(localized_subject, (str, type(None))):
            raise TypeError(
                f"Parameter `localized_subject` must be of type `str` or None, but got value `{localized_subject}` of type `{type(localized_subject).__name__}`"
            )
        self.localized_subject = localized_subject
        if not isinstance(image, int):
            raise TypeError(
                f"Parameter `image` must be of type `int`, but got value `{image}` of type `{type(image).__name__}`"
            )
        self.image = image
        if not isinstance(image_region, int):
            raise TypeError(
                f"Parameter `image_region` must be of type `int`, but got value `{image_region}` of type `{type(image_region).__name__}`"
            )
        self.image_region = image_region

        if user is not None and not isinstance(user, UserInfo):
            raise TypeError(
                f"Parameter `user` must be of type `UserInfo` or None, but got value `{user}` of type `{type(user).__name__}`"
            )
        self.user = user if user is not None else UserInfo()

        if not isinstance(visibility, int):
            raise TypeError(
                f"Parameter `visibility` must be of type `int`, but got value `{visibility}` of type `{type(visibility).__name__}`"
            )
        self.visibility = visibility

        if not isinstance(settings, (dict, type(None))):
            raise TypeError(
                f"Parameter `settings` must be of type `dict` or None, but got value `{settings}` of type `{type(settings).__name__}`"
            )
        self.settings = settings if settings is not None else {}

        if not isinstance(anonymous, bool):
            raise TypeError(
                f"Parameter `anonymous` must be of type `bool`, but got value `{anonymous}` of type `{type(anonymous).__name__}`"
            )
        self.anonymous = anonymous
        if not isinstance(multilingual, bool):
            raise TypeError(
                f"Parameter `multilingual` must be of type `bool`, but got value `{multilingual}` of type `{type(multilingual).__name__}`"
            )
        self.multilingual = multilingual


class ExperimentSettings:
    """General experiment settings and configuration."""

    creation_date: int
    speed: float
    speed_minimum: float
    speed_maximum: float
    speed_real: float
    paused: bool
    version: int
    camera_snapshot: Optional[CameraSave]
    plots: List[Any]
    widgets: List[Any]
    widget_groups: List[Any]
    bookmarks: Dict[str, Any]
    interfaces: Dict[str, bool]

    def __init__(
        self,
        creation_date: int = 0,
        speed: float = 1.0,
        speed_minimum: float = 0.0002,
        speed_maximum: float = 2.0,
        speed_real: float = 0.0,
        paused: bool = False,
        version: int = 0,
        camera_snapshot: Optional[CameraSave] = None,
        plots: Optional[List[Any]] = None,
        widgets: Optional[List[Any]] = None,
        widget_groups: Optional[List[Any]] = None,
        bookmarks: Optional[Dict[str, Any]] = None,
        interfaces: Optional[Dict[str, bool]] = None,
    ) -> None:
        if not isinstance(creation_date, int):
            raise TypeError(
                f"Parameter `creation_date` must be of type `int`, but got value `{creation_date}` of type `{type(creation_date).__name__}`"
            )
        self.creation_date = creation_date
        if not isinstance(speed, float):
            raise TypeError(
                f"Parameter `speed` must be of type `float`, but got value `{speed}` of type `{type(speed).__name__}`"
            )
        self.speed = speed
        if not isinstance(speed_minimum, float):
            raise TypeError(
                f"Parameter `speed_minimum` must be of type `float`, but got value `{speed_minimum}` of type `{type(speed_minimum).__name__}`"
            )
        self.speed_minimum = speed_minimum
        if not isinstance(speed_maximum, float):
            raise TypeError(
                f"Parameter `speed_maximum` must be of type `float`, but got value `{speed_maximum}` of type `{type(speed_maximum).__name__}`"
            )
        self.speed_maximum = speed_maximum
        if not isinstance(speed_real, float):
            raise TypeError(
                f"Parameter `speed_real` must be of type `float`, but got value `{speed_real}` of type `{type(speed_real).__name__}`"
            )
        self.speed_real = speed_real
        if not isinstance(paused, bool):
            raise TypeError(
                f"Parameter `paused` must be of type `bool`, but got value `{paused}` of type `{type(paused).__name__}`"
            )
        self.paused = paused
        if not isinstance(version, int):
            raise TypeError(
                f"Parameter `version` must be of type `int`, but got value `{version}` of type `{type(version).__name__}`"
            )
        self.version = version
        self.camera_snapshot = camera_snapshot

        if not isinstance(plots, (list, type(None))):
            raise TypeError(
                f"Parameter `plots` must be of type `list` or None, but got value `{plots}` of type `{type(plots).__name__}`"
            )
        self.plots = plots if plots is not None else []

        if not isinstance(widgets, (list, type(None))):
            raise TypeError(
                f"Parameter `widgets` must be of type `list` or None, but got value `{widgets}` of type `{type(widgets).__name__}`"
            )
        self.widgets = widgets if widgets is not None else []

        if not isinstance(widget_groups, (list, type(None))):
            raise TypeError(
                f"Parameter `widget_groups` must be of type `list` or None, but got value `{widget_groups}` of type `{type(widget_groups).__name__}`"
            )
        self.widget_groups = widget_groups if widget_groups is not None else []

        if not isinstance(bookmarks, (dict, type(None))):
            raise TypeError(
                f"Parameter `bookmarks` must be of type `dict` or None, but got value `{bookmarks}` of type `{type(bookmarks).__name__}`"
            )
        self.bookmarks = bookmarks if bookmarks is not None else {}

        if not isinstance(interfaces, (dict, type(None))):
            raise TypeError(
                f"Parameter `interfaces` must be of type `dict` or None, but got value `{interfaces}` of type `{type(interfaces).__name__}`"
            )
        self.interfaces = (
            interfaces
            if interfaces is not None
            else {"Play-Expanded": False, "Chart-Expanded": False}
        )


class CircuitTemplate:
    """Template for circuit experiments (Type 0)."""

    type: int
    experiment: ExperimentInfo
    id: None
    summary: Summary
    creation_date: int
    speed: float
    speed_minimum: float
    speed_maximum: float
    speed_real: float
    paused: bool
    version: int
    camera_snapshot: Optional[CameraSave]
    plots: List[Any]
    widgets: List[Any]
    widget_groups: List[Any]
    bookmarks: Dict[str, Any]
    interfaces: Dict[str, bool]

    def __init__(
        self,
        experiment_info: Optional[ExperimentInfo] = None,
        summary: Optional[Summary] = None,
        settings: Optional[ExperimentSettings] = None,
    ) -> None:
        self.type = 0

        if experiment_info is not None and not isinstance(
            experiment_info, ExperimentInfo
        ):
            raise TypeError(
                f"Parameter `experiment_info` must be of type `ExperimentInfo` or None, but got value `{experiment_info}` of type `{type(experiment_info).__name__}`"
            )
        self.experiment = (
            experiment_info
            if experiment_info is not None
            else ExperimentInfo(
                experiment_type=0,
                components=7,
                version=2404,
            )
        )

        self.id = None

        if summary is not None and not isinstance(summary, Summary):
            raise TypeError(
                f"Parameter `summary` must be of type `Summary` or None, but got value `{summary}` of type `{type(summary).__name__}`"
            )
        self.summary = (
            summary
            if summary is not None
            else Summary(
                summary_type=0,
                tags=["Type-0"],
                language="Chinese",
            )
        )

        if settings is not None and not isinstance(settings, ExperimentSettings):
            raise TypeError(
                f"Parameter `settings` must be of type `ExperimentSettings` or None, but got value `{settings}` of type `{type(settings).__name__}`"
            )
        experiment_settings = settings if settings is not None else ExperimentSettings()

        self.creation_date = experiment_settings.creation_date
        self.speed = experiment_settings.speed
        self.speed_minimum = experiment_settings.speed_minimum
        self.speed_maximum = experiment_settings.speed_maximum
        self.speed_real = experiment_settings.speed_real
        self.paused = experiment_settings.paused
        self.version = experiment_settings.version
        self.camera_snapshot = experiment_settings.camera_snapshot
        self.plots = experiment_settings.plots
        self.widgets = experiment_settings.widgets
        self.widget_groups = experiment_settings.widget_groups
        self.bookmarks = experiment_settings.bookmarks
        self.interfaces = experiment_settings.interfaces


class CelestialTemplate:
    """Template for celestial physics experiments (Type 3)."""

    type: int
    experiment: ExperimentInfo
    id: None
    summary: Summary
    creation_date: int
    speed: float
    speed_minimum: float
    speed_maximum: float
    speed_real: float
    paused: bool
    version: int
    camera_snapshot: Optional[CameraSave]
    plots: List[Any]
    widgets: List[Any]
    widget_groups: List[Any]
    bookmarks: Dict[str, Any]
    interfaces: Dict[str, bool]

    def __init__(
        self,
        experiment_info: Optional[ExperimentInfo] = None,
        summary: Optional[Summary] = None,
        settings: Optional[ExperimentSettings] = None,
    ) -> None:
        self.type = 3

        if experiment_info is not None and not isinstance(
            experiment_info, ExperimentInfo
        ):
            raise TypeError(
                f"Parameter `experiment_info` must be of type `ExperimentInfo` or None, but got value `{experiment_info}` of type `{type(experiment_info).__name__}`"
            )
        self.experiment = (
            experiment_info
            if experiment_info is not None
            else ExperimentInfo(
                experiment_type=3,
                components=0,
                version=2407,
            )
        )

        self.id = None

        if summary is not None and not isinstance(summary, Summary):
            raise TypeError(
                f"Parameter `summary` must be of type `Summary` or None, but got value `{summary}` of type `{type(summary).__name__}`"
            )
        self.summary = (
            summary
            if summary is not None
            else Summary(
                summary_type=3,
                tags=["Type-3"],
                language=None,
            )
        )

        if settings is not None and not isinstance(settings, ExperimentSettings):
            raise TypeError(
                f"Parameter `settings` must be of type `ExperimentSettings` or None, but got value `{settings}` of type `{type(settings).__name__}`"
            )
        experiment_settings = (
            settings
            if settings is not None
            else ExperimentSettings(
                speed_minimum=0.1,
                speed_maximum=10.0,
            )
        )

        self.creation_date = experiment_settings.creation_date
        self.speed = experiment_settings.speed
        self.speed_minimum = experiment_settings.speed_minimum
        self.speed_maximum = experiment_settings.speed_maximum
        self.speed_real = experiment_settings.speed_real
        self.paused = experiment_settings.paused
        self.version = experiment_settings.version
        self.camera_snapshot = experiment_settings.camera_snapshot
        self.plots = experiment_settings.plots
        self.widgets = experiment_settings.widgets
        self.widget_groups = experiment_settings.widget_groups
        self.bookmarks = experiment_settings.bookmarks
        self.interfaces = experiment_settings.interfaces


class ElectromagnetismTemplate:
    """Template for electromagnetism experiments (Type 4)."""

    type: int
    experiment: ExperimentInfo
    id: None
    summary: Summary
    creation_date: int
    speed: float
    speed_minimum: float
    speed_maximum: float
    speed_real: float
    paused: bool
    version: int
    camera_snapshot: Optional[CameraSave]
    plots: List[Any]
    widgets: List[Any]
    widget_groups: List[Any]
    bookmarks: Dict[str, Any]
    interfaces: Dict[str, bool]

    def __init__(
        self,
        experiment_info: Optional[ExperimentInfo] = None,
        summary: Optional[Summary] = None,
        settings: Optional[ExperimentSettings] = None,
    ) -> None:
        self.type = 4

        if experiment_info is not None and not isinstance(
            experiment_info, ExperimentInfo
        ):
            raise TypeError(
                f"Parameter `experiment_info` must be of type `ExperimentInfo` or None, but got value `{experiment_info}` of type `{type(experiment_info).__name__}`"
            )
        self.experiment = (
            experiment_info
            if experiment_info is not None
            else ExperimentInfo(
                experiment_type=4,
                components=1,
                version=2405,
            )
        )

        self.id = None

        if summary is not None and not isinstance(summary, Summary):
            raise TypeError(
                f"Parameter `summary` must be of type `Summary` or None, but got value `{summary}` of type `{type(summary).__name__}`"
            )
        self.summary = (
            summary
            if summary is not None
            else Summary(
                summary_type=4,
                tags=["Type-4"],
                language=None,
            )
        )

        if settings is not None and not isinstance(settings, ExperimentSettings):
            raise TypeError(
                f"Parameter `settings` must be of type `ExperimentSettings` or None, but got value `{settings}` of type `{type(settings).__name__}`"
            )
        experiment_settings = (
            settings
            if settings is not None
            else ExperimentSettings(
                speed_minimum=0.1,
                speed_maximum=2.0,
            )
        )

        self.creation_date = experiment_settings.creation_date
        self.speed = experiment_settings.speed
        self.speed_minimum = experiment_settings.speed_minimum
        self.speed_maximum = experiment_settings.speed_maximum
        self.speed_real = experiment_settings.speed_real
        self.paused = experiment_settings.paused
        self.version = experiment_settings.version
        self.camera_snapshot = experiment_settings.camera_snapshot
        self.plots = experiment_settings.plots
        self.widgets = experiment_settings.widgets
        self.widget_groups = experiment_settings.widget_groups
        self.bookmarks = experiment_settings.bookmarks
        self.interfaces = experiment_settings.interfaces


class CircuitExperiment:
    """Experimental support for circuit experiment."""

    wires: set
    _is_elementXYZ: bool
    _elementXYZ_origin_position: Any
    open_mode: Any
    _position2elements: Dict
    _id2element: Dict
    elements: List
    SAV_PATH: str
    pl_sav: dict
    camera_save: dict
    vision_center: Any
    target_rotation: Any

    def __init__(
        self,
        open_mode: Any,
        _position2elements: Dict,
        _id2element: Dict,
        Elements: List,
        SAV_PATH: str,
        PlSav: dict,
        CameraSave: dict,
        VisionCenter: Any,
        TargetRotation: Any,
        wires: set,
        is_elementXYZ: bool,
        elementXYZ_origin_position: Any,
    ) -> None:
        if not isinstance(SAV_PATH, str):
            raise TypeError(
                f"Parameter `SAV_PATH` must be of type `str`, but got value `{SAV_PATH}` of type `{type(SAV_PATH).__name__}`"
            )
        if not isinstance(wires, set):
            raise TypeError(
                f"Parameter `wires` must be of type `set`, but got value `{wires}` of type `{type(wires).__name__}`"
            )
        if not isinstance(is_elementXYZ, bool):
            raise TypeError(
                f"Parameter `is_elementXYZ` must be of type `bool`, but got value `{is_elementXYZ}` of type `{type(is_elementXYZ).__name__}`"
            )

        self.open_mode = open_mode
        self._position2elements = _position2elements
        self._id2element = _id2element
        self.elements = Elements
        self.SAV_PATH = SAV_PATH
        self.pl_sav = PlSav
        self.camera_save = CameraSave
        self.vision_center = VisionCenter
        self.target_rotation = TargetRotation
        self.wires = wires
        self._is_elementXYZ = is_elementXYZ
        self._elementXYZ_origin_position = elementXYZ_origin_position


class CelestialExperiment:
    """Experimental support for celestial experiment."""

    open_mode: Any
    _position2elements: Dict
    _id2element: Dict
    elements: List
    SAV_PATH: str
    pl_sav: dict
    camera_save: dict
    vision_center: Any
    target_rotation: Any

    def __init__(
        self,
        open_mode: Any,
        _position2elements: Dict,
        _id2element: Dict,
        Elements: List,
        SAV_PATH: str,
        PlSav: dict,
        CameraSave: dict,
        VisionCenter: Any,
        TargetRotation: Any,
    ) -> None:
        if not isinstance(SAV_PATH, str):
            raise TypeError(
                f"Parameter `SAV_PATH` must be of type `str`, but got value `{SAV_PATH}` of type `{type(SAV_PATH).__name__}`"
            )

        self.open_mode = open_mode
        self._position2elements = _position2elements
        self._id2element = _id2element
        self.elements = Elements
        self.SAV_PATH = SAV_PATH
        self.pl_sav = PlSav
        self.camera_save = CameraSave
        self.vision_center = VisionCenter
        self.target_rotation = TargetRotation


class ElectromagnetismExperiment:
    """Experimental support for electromagnetism experiment."""

    open_mode: Any
    _position2elements: Dict
    _id2element: Dict
    elements: List
    SAV_PATH: str
    pl_sav: dict
    camera_save: dict
    vision_center: Any
    target_rotation: Any

    def __init__(
        self,
        open_mode: Any,
        _position2elements: Dict,
        _id2element: Dict,
        Elements: List,
        SAV_PATH: str,
        PlSav: dict,
        CameraSave: dict,
        VisionCenter: Any,
        TargetRotation: Any,
    ) -> None:
        if not isinstance(SAV_PATH, str):
            raise TypeError(
                f"Parameter `SAV_PATH` must be of type `str`, but got value `{SAV_PATH}` of type `{type(SAV_PATH).__name__}`"
            )

        self.open_mode = open_mode
        self._position2elements = _position2elements
        self._id2element = _id2element
        self.elements = Elements
        self.SAV_PATH = SAV_PATH
        self.pl_sav = PlSav
        self.camera_save = CameraSave
        self.vision_center = VisionCenter
        self.target_rotation = TargetRotation
