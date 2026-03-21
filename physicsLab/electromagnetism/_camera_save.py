import json
from physicsLab._typing import num_type
from physicsLab import coordinate_system


class CameraSave:
    __distance: num_type
    __vision_center: coordinate_system.Position
    __target_rotation: coordinate_system.Rotation

    def __init__(
        self,
        distance: num_type = 2,
        vision_center: coordinate_system.Position = coordinate_system.Position(
            0, 0, 0.88
        ),
        target_rotation: coordinate_system.Rotation = coordinate_system.Rotation(
            90, 0, 0
        ),
    ) -> None:
        self.distance = distance
        self.vision_center = vision_center
        self.target_rotation = target_rotation

    @property
    def distance(self) -> num_type:
        return self.__distance

    @distance.setter
    def distance(self, distance: num_type) -> None:
        if not isinstance(distance, (int, float)):
            raise TypeError(
                f"distance must be of type `int | float`, but got value {distance} of type {type(distance).__name__}"
            )

        self.__distance = distance

    @property
    def vision_center(self) -> coordinate_system.Position:
        return self.__vision_center

    @vision_center.setter
    def vision_center(self, vision_center: coordinate_system.Position) -> None:
        if not isinstance(vision_center, coordinate_system.Position):
            raise TypeError(
                f"vision_center must be of type `Position`, but got value {vision_center} of type {type(vision_center).__name__}"
            )

        self.__vision_center = vision_center

    @property
    def target_rotation(self) -> coordinate_system.Rotation:
        return self.__target_rotation

    @target_rotation.setter
    def target_rotation(self, target_rotation: coordinate_system.Rotation) -> None:
        if not isinstance(target_rotation, coordinate_system.Rotation):
            raise TypeError(
                f"target_rotation must be of type `Rotation`, but got value {target_rotation} of type {type(target_rotation).__name__}"
            )

        self.__target_rotation = target_rotation

    def as_dict(self) -> dict:
        return {
            "Mode": 1,
            "Distance": self.distance,
            "VisionCenter": self.vision_center.as_postion_str_in_plsav(),
            "TargetRotation": self.target_rotation.as_rotation_str_in_plsav(),
        }

    def as_str_in_plsav(self) -> str:
        return json.dumps(self.as_dict())
