# -*- coding: utf-8 -*-
from physicsLab.savTemplate import Generate
from ._electromagnetismBase import ElectromagnetismBase
from physicsLab._core import _Experiment
from physicsLab._typing import (
    num_type,
    Optional,
    final,
)


class Negative_Charge(ElectromagnetismBase):
    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        /,
        *,
        identifier: Optional[str] = None,
        experiment: Optional[_Experiment] = None,
    ) -> None:
        super().__init__(x, y, z, identifier=identifier, experiment=experiment)

    @property
    def data(self):
        return self.as_dict()

    def as_dict(self):
        return {
            "ModelID": "Negative Charge",
            "Identifier": self.identifier,
            "Properties": {"锁定": 1.0, "强度": -1e-07, "质量": 0.1},
            "Position": self._position.as_postion_str_in_plsav(),
            "Rotation": self._rotation.as_rotation_str_in_plsav(),
            "Velocity": "0,0,0",
            "AngularVelocity": "0,0,0",
        }

    @final
    @staticmethod
    def zh_name() -> str:
        return "负电荷"


class Positive_Charge(ElectromagnetismBase):
    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        /,
        *,
        identifier: Optional[str] = None,
        experiment: Optional[_Experiment] = None,
    ) -> None:
        super().__init__(x, y, z, identifier=identifier, experiment=experiment)

    @property
    def data(self):
        return self.as_dict()

    def as_dict(self):
        return {
            "ModelID": "Positive Charge",
            "Identifier": self.identifier,
            "Properties": {"锁定": 1.0, "强度": 1e-07, "质量": 0.1},
            "Position": self._position.as_postion_str_in_plsav(),
            "Rotation": self._rotation.as_rotation_str_in_plsav(),
            "Velocity": "0,0,0",
            "AngularVelocity": "0,0,0",
        }

    @final
    @staticmethod
    def zh_name() -> str:
        return "正电荷"


class Negative_Test_Charge(ElectromagnetismBase):
    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        /,
        *,
        identifier: Optional[str] = None,
        experiment: Optional[_Experiment] = None,
    ) -> None:
        super().__init__(x, y, z, identifier=identifier, experiment=experiment)

    @property
    def data(self):
        return self.as_dict()

    def as_dict(self):
        return {
            "ModelID": "Negative Test Charge",
            "Identifier": self.identifier,
            "Properties": {"锁定": 0.0, "强度": -1e-10, "质量": 5e-06},
            "Position": self._position.as_postion_str_in_plsav(),
            "Rotation": self._rotation.as_rotation_str_in_plsav(),
            "Velocity": "0,0,0",
            "AngularVelocity": "0,0,0",
        }

    @final
    @staticmethod
    def zh_name() -> str:
        return "正试验电荷"


class Positive_Test_Charge(ElectromagnetismBase):
    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        /,
        *,
        identifier: Optional[str] = None,
        experiment: Optional[_Experiment] = None,
    ) -> None:
        super().__init__(x, y, z, identifier=identifier, experiment=experiment)

    @property
    def data(self):
        return self.as_dict()

    def as_dict(self):
        return {
            "ModelID": "Positive Test Charge",
            "Identifier": self.identifier,
            "Properties": {"锁定": 0.0, "强度": -1e-10, "质量": 5e-06},
            "Position": self._position.as_postion_str_in_plsav(),
            "Rotation": self._rotation.as_rotation_str_in_plsav(),
            "Velocity": "0,0,0",
            "AngularVelocity": "0,0,0",
        }

    @final
    @staticmethod
    def zh_name() -> str:
        return "负试验电荷"


class Bar_Magnet(ElectromagnetismBase):
    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        /,
        *,
        identifier: Optional[str] = None,
        experiment: Optional[_Experiment] = None,
    ) -> None:
        super().__init__(x, y, z, identifier=identifier, experiment=experiment)

    @property
    def data(self):
        return self.as_dict()

    def as_dict(self):
        return {
            "ModelID": "Bar Magnet",
            "Identifier": self.identifier,
            "Properties": {"锁定": 1.0, "强度": 1.0, "质量": 10.0},
            "Position": self._position.as_postion_str_in_plsav(),
            "Rotation": self._rotation.as_rotation_str_in_plsav(),
            "Velocity": "0,0,0",
            "AngularVelocity": "0,0,0",
        }

    @final
    @staticmethod
    def zh_name() -> str:
        return "条形磁铁"


class Compass(ElectromagnetismBase):
    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        /,
        *,
        identifier: Optional[str] = None,
        experiment: Optional[_Experiment] = None,
    ) -> None:
        super().__init__(x, y, z, identifier=identifier, experiment=experiment)

    @property
    def data(self):
        return self.as_dict()

    def as_dict(self):
        return {
            "ModelID": "Compass",
            "Identifier": self.identifier,
            "Properties": {"锁定": 1.0},
            "Position": self._position.as_postion_str_in_plsav(),
            "Rotation": self._rotation.as_rotation_str_in_plsav(),
            "Velocity": "0,0,0",
            "AngularVelocity": "0,0,0",
        }

    @final
    @staticmethod
    def zh_name() -> str:
        return "指南针"


class Uniform_Magnetic_Field(ElectromagnetismBase):
    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        /,
        *,
        identifier: Optional[str] = None,
        experiment: Optional[_Experiment] = None,
    ) -> None:
        super().__init__(x, y, z, identifier=identifier, experiment=experiment)

    @property
    def data(self):
        return self.as_dict()

    def as_dict(self):
        return {
            "ModelID": "Uniform Magnetic Field",
            "Identifier": self.identifier,
            "Properties": {"锁定": 0.0, "强度": 1000.0, "方向": 1.0},
            "Position": self._position.as_postion_str_in_plsav(),
            "Rotation": self._rotation.as_rotation_str_in_plsav(),
            "Velocity": "0,0,0",
            "AngularVelocity": "0,0,0",
        }

    @final
    @staticmethod
    def zh_name() -> str:
        return "匀强磁场"
