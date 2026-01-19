# -*- coding: utf-8 -*-

from typing import Optional, List, Dict, Any
from physicsLab._typing import num_type
from physicsLab.web.api import User


class Generate:
    """Placeholder class indicating that the corresponding key's value is dynamically generated at runtime.
    If the corresponding value is not generated at runtime, an error will occur when generating JSON.
    """


def _validate_str(
    value: Any, param_name: str, allow_none: bool = True
) -> Optional[str]:
    """Validate string parameter."""
    if value is None and allow_none:
        return None
    if not isinstance(value, str):
        raise TypeError(
            f"Parameter `{param_name}` must be of type `str` or None, but got value `{value}` of type `{type(value).__name__}`"
        )
    return value


def _validate_int(value: Any, param_name: str) -> int:
    """Validate integer parameter."""
    if not isinstance(value, int):
        raise TypeError(
            f"Parameter `{param_name}` must be of type `int`, but got value `{value}` of type `{type(value).__name__}`"
        )
    return value


def _validate_float(value: Any, param_name: str) -> float:
    """Validate float parameter."""
    if not isinstance(value, float):
        raise TypeError(
            f"Parameter `{param_name}` must be of type `float`, but got value `{value}` of type `{type(value).__name__}`"
        )
    return value


def _validate_bool(value: Any, param_name: str) -> bool:
    """Validate boolean parameter."""
    if not isinstance(value, bool):
        raise TypeError(
            f"Parameter `{param_name}` must be of type `bool`, but got value `{value}` of type `{type(value).__name__}`"
        )
    return value


def _validate_list(
    value: Any, param_name: str, allow_none: bool = True
) -> Optional[List]:
    """Validate list parameter."""
    if value is None and allow_none:
        return None
    if not isinstance(value, list):
        raise TypeError(
            f"Parameter `{param_name}` must be of type `list` or None, but got value `{value}` of type `{type(value).__name__}`"
        )
    return value


def _validate_dict(
    value: Any, param_name: str, allow_none: bool = True
) -> Optional[Dict[str, Any]]:
    """Validate dictionary parameter."""
    if value is None and allow_none:
        return None
    if not isinstance(value, dict):
        raise TypeError(
            f"Parameter `{param_name}` must be of type `dict` or None, but got value `{value}` of type `{type(value).__name__}`"
        )
    return value


class ExperimentInfo:
    """Experiment metadata information."""

    def __init__(
        self,
        experiment_id: Optional[str] = None,
        experiment_type: int = 0,
        components: int = 0,
        subject: Optional[str] = None,
        status_save: Any = Generate,
        camera_save: Any = Generate,
        version: int = 2404,
        creation_date: Any = Generate,
        paused: bool = False,
        summary: Optional[Any] = None,
        plots: Optional[Any] = None,
    ) -> None:
        self.ID = _validate_str(experiment_id, "experiment_id")
        self.Type = _validate_int(experiment_type, "experiment_type")
        self.Components = _validate_int(components, "components")
        self.Subject = _validate_str(subject, "subject")
        self.StatusSave = status_save
        self.CameraSave = camera_save
        self.Version = _validate_int(version, "version")
        self.CreationDate = creation_date
        self.Paused = _validate_bool(paused, "paused")
        self.Summary = summary
        self.Plots = plots


class UserInfo:
    """User information embedded in experiment summary."""

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
        self.ID = _validate_str(user_id, "user_id")
        self.Nickname = _validate_str(nickname, "nickname")
        self.Signature = _validate_str(signature, "signature")
        self.Avatar = _validate_int(avatar, "avatar")
        self.AvatarRegion = _validate_int(avatar_region, "avatar_region")
        self.Decoration = _validate_int(decoration, "decoration")
        self.Verification = _validate_str(verification, "verification")


class Summary:
    """Experiment summary information for publication."""

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
        creation_date: Any = Generate,
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
        self.Type = _validate_int(summary_type, "summary_type")
        self.ParentID = _validate_str(parent_id, "parent_id")
        self.ParentName = _validate_str(parent_name, "parent_name")
        self.ParentCategory = _validate_str(parent_category, "parent_category")
        self.ContentID = _validate_str(content_id, "content_id")
        self.Editor = _validate_str(editor, "editor")

        coauthors = _validate_list(coauthors, "coauthors")
        self.Coauthors = coauthors if coauthors is not None else []

        self.Description = _validate_str(description, "description")
        self.LocalizedDescription = _validate_str(
            localized_description, "localized_description"
        )

        tags = _validate_list(tags, "tags")
        self.Tags = tags if tags is not None else [f"Type-{summary_type}"]

        self.ModelID = _validate_str(model_id, "model_id")
        self.ModelName = _validate_str(model_name, "model_name")

        model_tags = _validate_list(model_tags, "model_tags")
        self.ModelTags = model_tags if model_tags is not None else []

        self.Version = _validate_int(version, "version")
        self.Language = _validate_str(language, "language", allow_none=True)
        self.Visits = _validate_int(visits, "visits")
        self.Stars = _validate_int(stars, "stars")
        self.Supports = _validate_int(supports, "supports")
        self.Remixes = _validate_int(remixes, "remixes")
        self.Comments = _validate_int(comments, "comments")
        self.Price = _validate_int(price, "price")
        self.Popularity = _validate_int(popularity, "popularity")
        self.CreationDate = creation_date
        self.UpdateDate = _validate_int(update_date, "update_date")
        self.SortingDate = _validate_int(sorting_date, "sorting_date")
        self.ID = _validate_str(summary_id, "summary_id")
        self.Category = _validate_str(category, "category")
        self.Subject = _validate_str(subject, "subject")
        self.LocalizedSubject = _validate_str(localized_subject, "localized_subject")
        self.Image = _validate_int(image, "image")
        self.ImageRegion = _validate_int(image_region, "image_region")

        if user is not None and not isinstance(user, UserInfo):
            raise TypeError(
                f"Parameter `user` must be of type `UserInfo` or None, but got value `{user}` of type `{type(user).__name__}`"
            )
        self.User = user if user is not None else UserInfo()

        self.Visibility = _validate_int(visibility, "visibility")

        settings = _validate_dict(settings, "settings")
        self.Settings = settings if settings is not None else {}

        self.Anonymous = _validate_bool(anonymous, "anonymous")
        self.Multilingual = _validate_bool(multilingual, "multilingual")


class ExperimentSettings:
    """General experiment settings and configuration."""

    def __init__(
        self,
        creation_date: int = 0,
        speed: float = 1.0,
        speed_minimum: float = 0.0002,
        speed_maximum: float = 2.0,
        speed_real: float = 0.0,
        paused: bool = False,
        version: int = 0,
        camera_snapshot: Optional[Any] = None,
        plots: Optional[List[Any]] = None,
        widgets: Optional[List[Any]] = None,
        widget_groups: Optional[List[Any]] = None,
        bookmarks: Optional[Dict[str, Any]] = None,
        interfaces: Optional[Dict[str, bool]] = None,
    ) -> None:
        self.CreationDate = _validate_int(creation_date, "creation_date")
        self.Speed = _validate_float(speed, "speed")
        self.SpeedMinimum = _validate_float(speed_minimum, "speed_minimum")
        self.SpeedMaximum = _validate_float(speed_maximum, "speed_maximum")
        self.SpeedReal = _validate_float(speed_real, "speed_real")
        self.Paused = _validate_bool(paused, "paused")
        self.Version = _validate_int(version, "version")
        self.CameraSnapshot = camera_snapshot

        plots = _validate_list(plots, "plots")
        self.Plots = plots if plots is not None else []

        widgets = _validate_list(widgets, "widgets")
        self.Widgets = widgets if widgets is not None else []

        widget_groups = _validate_list(widget_groups, "widget_groups")
        self.WidgetGroups = widget_groups if widget_groups is not None else []

        bookmarks = _validate_dict(bookmarks, "bookmarks")
        self.Bookmarks = bookmarks if bookmarks is not None else {}

        interfaces = _validate_dict(interfaces, "interfaces")
        self.Interfaces = (
            interfaces
            if interfaces is not None
            else {"Play-Expanded": False, "Chart-Expanded": False}
        )


class CircuitTemplate:
    """Template for circuit experiments (Type 0)."""

    def __init__(
        self,
        experiment_info: Optional[ExperimentInfo] = None,
        summary: Optional[Summary] = None,
        settings: Optional[ExperimentSettings] = None,
    ) -> None:
        self.Type = 0

        if experiment_info is not None and not isinstance(
            experiment_info, ExperimentInfo
        ):
            raise TypeError(
                f"Parameter `experiment_info` must be of type `ExperimentInfo` or None, but got value `{experiment_info}` of type `{type(experiment_info).__name__}`"
            )
        self.Experiment = (
            experiment_info
            if experiment_info is not None
            else ExperimentInfo(
                experiment_type=0,
                components=7,
                version=2404,
            )
        )

        self.ID = None

        if summary is not None and not isinstance(summary, Summary):
            raise TypeError(
                f"Parameter `summary` must be of type `Summary` or None, but got value `{summary}` of type `{type(summary).__name__}`"
            )
        self.Summary = (
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

        self.CreationDate = experiment_settings.CreationDate
        self.Speed = experiment_settings.Speed
        self.SpeedMinimum = experiment_settings.SpeedMinimum
        self.SpeedMaximum = experiment_settings.SpeedMaximum
        self.SpeedReal = experiment_settings.SpeedReal
        self.Paused = experiment_settings.Paused
        self.Version = experiment_settings.Version
        self.CameraSnapshot = experiment_settings.CameraSnapshot
        self.Plots = experiment_settings.Plots
        self.Widgets = experiment_settings.Widgets
        self.WidgetGroups = experiment_settings.WidgetGroups
        self.Bookmarks = experiment_settings.Bookmarks
        self.Interfaces = experiment_settings.Interfaces


class CelestialTemplate:
    """Template for celestial physics experiments (Type 3)."""

    def __init__(
        self,
        experiment_info: Optional[ExperimentInfo] = None,
        summary: Optional[Summary] = None,
        settings: Optional[ExperimentSettings] = None,
    ) -> None:
        self.Type = 3

        if experiment_info is not None and not isinstance(
            experiment_info, ExperimentInfo
        ):
            raise TypeError(
                f"Parameter `experiment_info` must be of type `ExperimentInfo` or None, but got value `{experiment_info}` of type `{type(experiment_info).__name__}`"
            )
        self.Experiment = (
            experiment_info
            if experiment_info is not None
            else ExperimentInfo(
                experiment_type=3,
                components=0,
                version=2407,
            )
        )

        self.ID = None

        if summary is not None and not isinstance(summary, Summary):
            raise TypeError(
                f"Parameter `summary` must be of type `Summary` or None, but got value `{summary}` of type `{type(summary).__name__}`"
            )
        self.Summary = (
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

        self.CreationDate = experiment_settings.CreationDate
        self.Speed = experiment_settings.Speed
        self.SpeedMinimum = experiment_settings.SpeedMinimum
        self.SpeedMaximum = experiment_settings.SpeedMaximum
        self.SpeedReal = experiment_settings.SpeedReal
        self.Paused = experiment_settings.Paused
        self.Version = experiment_settings.Version
        self.CameraSnapshot = experiment_settings.CameraSnapshot
        self.Plots = experiment_settings.Plots
        self.Widgets = experiment_settings.Widgets
        self.WidgetGroups = experiment_settings.WidgetGroups
        self.Bookmarks = experiment_settings.Bookmarks
        self.Interfaces = experiment_settings.Interfaces


class ElectromagnetismTemplate:
    """Template for electromagnetism experiments (Type 4)."""

    def __init__(
        self,
        experiment_info: Optional[ExperimentInfo] = None,
        summary: Optional[Summary] = None,
        settings: Optional[ExperimentSettings] = None,
    ) -> None:
        self.Type = 4

        if experiment_info is not None and not isinstance(
            experiment_info, ExperimentInfo
        ):
            raise TypeError(
                f"Parameter `experiment_info` must be of type `ExperimentInfo` or None, but got value `{experiment_info}` of type `{type(experiment_info).__name__}`"
            )
        self.Experiment = (
            experiment_info
            if experiment_info is not None
            else ExperimentInfo(
                experiment_type=4,
                components=1,
                version=2405,
            )
        )

        self.ID = None

        if summary is not None and not isinstance(summary, Summary):
            raise TypeError(
                f"Parameter `summary` must be of type `Summary` or None, but got value `{summary}` of type `{type(summary).__name__}`"
            )
        self.Summary = (
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

        self.CreationDate = experiment_settings.CreationDate
        self.Speed = experiment_settings.Speed
        self.SpeedMinimum = experiment_settings.SpeedMinimum
        self.SpeedMaximum = experiment_settings.SpeedMaximum
        self.SpeedReal = experiment_settings.SpeedReal
        self.Paused = experiment_settings.Paused
        self.Version = experiment_settings.Version
        self.CameraSnapshot = experiment_settings.CameraSnapshot
        self.Plots = experiment_settings.Plots
        self.Widgets = experiment_settings.Widgets
        self.WidgetGroups = experiment_settings.WidgetGroups
        self.Bookmarks = experiment_settings.Bookmarks
        self.Interfaces = experiment_settings.Interfaces


class CircuitExperiment:
    """Experimental support for circuit experiment."""

    Wires: set
    _is_elementXYZ: bool
    _elementXYZ_origin_position: Any

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
        self.Elements = Elements
        self.SAV_PATH = SAV_PATH
        self.PlSav = PlSav
        self.CameraSave = CameraSave
        self.VisionCenter = VisionCenter
        self.TargetRotation = TargetRotation
        self.Wires = wires
        self._is_elementXYZ = is_elementXYZ
        self._elementXYZ_origin_position = elementXYZ_origin_position


class CelestialExperiment:
    """Experimental support for celestial experiment."""

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
        self.Elements = Elements
        self.SAV_PATH = SAV_PATH
        self.PlSav = PlSav
        self.CameraSave = CameraSave
        self.VisionCenter = VisionCenter
        self.TargetRotation = TargetRotation


class ElectromagnetismExperiment:
    """Experimental support for electromagnetism experiment."""

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
        self.Elements = Elements
        self.SAV_PATH = SAV_PATH
        self.PlSav = PlSav
        self.CameraSave = CameraSave
        self.VisionCenter = VisionCenter
        self.TargetRotation = TargetRotation
