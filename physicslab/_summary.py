import time
from physicslab import enums
from physicslab._typing import Optional, Set
from physicslab.errors import ExperimentTypeError
from physicslab._experiment import (
    serialize_introduction,
    deserialize_introduction,
    serialize_tags,
    construct_tags,
)

class Summary:
    """Summary information about an experiment, as displayed in Physics-Lab-AR."""

    __experiment_type: int
    __subject: Optional[str]
    __description: Optional[str]
    __tags: Set[enums.Tag]
    __type_tag: str

    def __init__(
        self,
        experiment_type: int,
        subject: Optional[str],
        description: Optional[str],
        tags: Set[enums.Tag],
        type_tag: str,
    ) -> None:
        self.experiment_type = experiment_type
        self.subject = subject
        self.description = description
        self.tags = set() if tags is None else tags
        self.type_tag = type_tag

    @property
    def experiment_type(self) -> int:
        return self.__experiment_type

    @experiment_type.setter
    def experiment_type(self, experiment_type: int) -> None:
        if not isinstance(experiment_type, int):
            raise TypeError(
                f"experiment_type must be of type `int`, but got value {experiment_type} of type {type(experiment_type).__name__}"
            )
        self.__experiment_type = experiment_type

    @property
    def subject(self) -> Optional[str]:
        return self.__subject

    @subject.setter
    def subject(self, subject: Optional[str]) -> None:
        if not isinstance(subject, (str, type(None))):
            raise TypeError(
                f"subject must be of type `str | None`, but got value {subject} of type {type(subject).__name__}"
            )
        self.__subject = subject

    @property
    def description(self) -> Optional[str]:
        return self.__description

    @description.setter
    def description(self, description: Optional[str]) -> None:
        if not isinstance(description, (str, type(None))):
            raise TypeError(
                f"description must be of type `str | None`, but got value {description} of type {type(description).__name__}"
            )
        self.__description = description

    @property
    def tags(self) -> Set[enums.Tag]:
        return self.__tags.copy()

    @tags.setter
    def tags(self, tags: Set[enums.Tag]) -> None:
        if not isinstance(tags, set):
            raise TypeError(
                f"tags must be of type `set[Tag]`, but got value {tags} of type {type(tags).__name__}"
            )
        if not all(isinstance(tag, enums.Tag) for tag in tags):
            raise TypeError(
                f"tags must be of type `set[Tag]`, but got value {tags} of type `set` containing non-Tag elements"
            )
        self.__tags = tags.copy()

    @property
    def type_tag(self) -> str:
        return self.__type_tag

    @type_tag.setter
    def type_tag(self, type_tag: str) -> None:
        if not isinstance(type_tag, str):
            raise TypeError(
                f"type_tag must be of type `str`, but got value {type_tag} of type {type(type_tag).__name__}"
            )
        self.__type_tag = type_tag

    def as_dict(self) -> dict:
        creation_date = int(time.time() * 1000)
        return {
            "Type": self.experiment_type,
            "ParentID": None,
            "ParentName": None,
            "ParentCategory": None,
            "ContentID": None,
            "Editor": None,
            "Coauthors": [],
            "Description": serialize_introduction(self.description),
            "LocalizedDescription": None,
            "Tags": serialize_tags(self.tags, type_tag=self.type_tag),
            "ModelID": None,
            "ModelName": None,
            "ModelTags": [],
            "Version": 0,
            "Language": None,
            "Visits": 0,
            "Stars": 0,
            "Supports": 0,
            "Remixes": 0,
            "Comments": 0,
            "Price": 0,
            "Popularity": 0,
            "CreationDate": creation_date,
            "UpdateDate": 0,
            "SortingDate": 0,
            "ID": None,
            "Category": None,
            "Subject": self.subject,
            "LocalizedSubject": None,
            "Image": 0,
            "ImageRegion": 0,
            "User": {
                "ID": None,
                "Nickname": None,
                "Signature": None,
                "Avatar": 0,
                "AvatarRegion": 0,
                "Decoration": 0,
                "Verification": None,
            },
            "Visibility": 0,
            "Settings": {},
            "Multilingual": False,
        }


def construct_summary_from_plsav_dict(
    summary_dict: Optional[dict],
    experiment_type: int,
    type_tag: str,
) -> Summary:
    if not isinstance(experiment_type, int):
        raise TypeError(
            f"experiment_type must be of type `int`, but got value {experiment_type} of type {type(experiment_type).__name__}"
        )
    if summary_dict is None:
        return Summary(
            experiment_type=experiment_type,
            subject=None,
            description=None,
            tags=set(),
            type_tag=type_tag,
        )
    if not isinstance(summary_dict, dict):
        raise TypeError(
            f"summary_dict must be of type `dict | None`, but got value {summary_dict} of type {type(summary_dict).__name__}"
        )
    if summary_dict["Type"] != experiment_type:
        raise ExperimentTypeError(
            f'summary["Type"] ({summary_dict["Type"]}) does not match experiment_type ({experiment_type})'
        )

    return Summary(
        experiment_type=experiment_type,
        subject=summary_dict.get("Subject"),
        description=deserialize_introduction(summary_dict.get("Description")),
        tags=construct_tags(summary_dict.get("Tags"), type_tag=type_tag),
        type_tag=type_tag,
    )
