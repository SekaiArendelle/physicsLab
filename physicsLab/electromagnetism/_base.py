# -*- coding: utf-8 -*-
from physicsLab import coordinate_system


class ElectromagnetismBase:
    """Base class for electromagnetism elements"""

    __position: coordinate_system.Position
    __rotation: coordinate_system.Rotation
    __identifier: str

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation,
        identifier: str,
    ) -> None:
        self.position = position
        self.rotation = rotation
        self.identifier = identifier

    @property
    def identifier(self) -> str:
        return self.__identifier

    @identifier.setter
    def identifier(self, identifier: str) -> None:
        if not isinstance(identifier, str):
            raise TypeError(
                f"identifier must be of type `str`, but got value {identifier} of type {type(identifier).__name__}"
            )

        self.__identifier = identifier

    @property
    def position(self) -> coordinate_system.Position:
        return self.__position

    @position.setter
    def position(self, position: coordinate_system.Position) -> None:
        if not isinstance(position, coordinate_system.Position):
            raise TypeError(
                f"position must be of type `Position`, but got value {position} of type {type(position).__name__}"
            )

        self.__position = position

    @property
    def rotation(self) -> coordinate_system.Rotation:
        return self.__rotation

    @rotation.setter
    def rotation(self, rotation: coordinate_system.Rotation) -> None:
        if not isinstance(rotation, coordinate_system.Rotation):
            raise TypeError(
                f"rotation must be of type `Rotation`, but got value {rotation} of type {type(rotation).__name__}"
            )

        self.__rotation = rotation
