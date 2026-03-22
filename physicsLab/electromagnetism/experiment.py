import time
from ._camera_save import CameraSave
from ._status_save import ElectromagnetismStatusSave
from ._base import ElectromagnetismBase
from physicsLab._typing import Self

class ElectromagnetismExperiment:
    __status_save: ElectromagnetismStatusSave
    __camera_save: CameraSave

    def __init__(self, camera_save: CameraSave = CameraSave()) -> None:
        self.status_save = ElectromagnetismStatusSave()
        self.camera_save = camera_save

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        pass

    @property
    def camera_save(self) -> CameraSave:
        return self.__camera_save

    @camera_save.setter
    def camera_save(self, camera_save: CameraSave) -> None:
        if not isinstance(camera_save, CameraSave):
            raise TypeError(
                f"camera_save must be of type `CameraSave`, but got value {camera_save} of type {type(camera_save).__name__}"
            )

        self.__camera_save = camera_save

    @property
    def status_save(self) -> ElectromagnetismStatusSave:
        return self.__status_save

    @status_save.setter
    def status_save(self, status_save: ElectromagnetismStatusSave) -> None:
        if not isinstance(status_save, ElectromagnetismStatusSave):
            raise TypeError(
                f"status_save must be of type `StatusSave`, but got value {status_save} of type {type(status_save).__name__}"
            )

        self.__status_save = status_save

    def _crt_a_element(self, element: ElectromagnetismBase) -> None:
        self.status_save.append_element(element)

    def crt_elements(self, *elements: ElectromagnetismBase) -> Self:
        for element in elements:
            self._crt_a_element(element)

        return self

    def as_plsav_dict(self) -> dict:
        return {
            "Type": 4,
            "Experiment": {
                "ID": None,
                "Type": 4,
                "Components": len(self.status_save.elements),
                "Subject": None,
                "StatusSave": self.status_save.as_str_in_plsav(),
                "CameraSave": self.camera_save.as_str_in_plsav(),
                "Version": 2405,
                "CreationDate": int(time.time() * 1000),
                "Paused": False,
                "Summary": None,
                "Plots": None,
            },
            "ID": None,
            "Summary": {
                "Type": 4,
                "ParentID": None,
                "ParentName": None,
                "ParentCategory": None,
                "ContentID": None,
                "Editor": None,
                "Coauthors": [],
                "Description": None,
                "LocalizedDescription": None,
                "Tags": ["Type-4"],
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
                "CreationDate": int(time.time() * 1000),
                "UpdateDate": 0,
                "SortingDate": 0,
                "ID": None,
                "Category": None,
                "Subject": None,
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
            },
            "CreationDate": 0,
            "Speed": 1.0,
            "SpeedMinimum": 0.1,
            "SpeedMaximum": 2.0,
            "SpeedReal": 0.0,
            "Paused": False,
            "Version": 0,
            "CameraSnapshot": None,
            "Plots": [],
            "Widgets": [],
            "WidgetGroups": [],
            "Bookmarks": {},
            "Interfaces": {"Play-Expanded": False, "Chart-Expanded": False},
        }
