# -*- coding: utf-8 -*-
from physicsLab import _tools
from physicsLab import errors
from physicsLab import coordinate_system
from physicsLab.enums import ExperimentType
from physicsLab._core import get_current_experiment, _Experiment, ElementBase
from physicsLab._typing import num_type, Self, override, NoReturn, Optional


class ElectromagnetismBase(ElementBase):
    """所有电与磁元件的父类"""

    experiment: _Experiment

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
        if not isinstance(x, (int, float)):
            raise TypeError(
                f"Parameter x must be of type `int | float`, but got {type(x).__name__}"
            )
        if not isinstance(y, (int, float)):
            raise TypeError(
                f"Parameter y must be of type `int | float`, but got {type(y).__name__}"
            )
        if not isinstance(z, (int, float)):
            raise TypeError(
                f"Parameter z must be of type `int | float`, but got {type(z).__name__}"
            )
        if not isinstance(identifier, (str, type(None))):
            raise TypeError(
                f"Parameter identifier must be of type `Optional[str]`, but got {type(identifier).__name__}"
            )
        if not isinstance(experiment, (_Experiment, type(None))):
            raise TypeError(
                f"Parameter experiment must be of type `Optional[Experiment]`, but got {type(experiment).__name__}"
            )

        _Expe: _Experiment
        if experiment is None:
            _Expe = get_current_experiment()
        else:
            _Expe = experiment
        if _Expe.experiment_type != ExperimentType.Electromagnetism:
            raise errors.ExperimentTypeError(
                f"Can't create {self.__class__.__name__} because experiment_type is {_Expe.experiment_type}"
            )

        self.experiment = _Expe
        self.identifier = identifier if identifier is not None else _tools.randString(33)
        self.set_position(x, y, z)
        self.set_rotation(0, 0, 0)

        self.experiment.Elements.append(self)
        self.experiment._id2element[self.identifier] = self

    @override
    def set_position(self, x: num_type, y: num_type, z: num_type) -> Self:
        if (
            not isinstance(x, (int, float))
            or not isinstance(y, (int, float))
            or not isinstance(z, (int, float))
        ):
            raise TypeError

        x, y, z = _tools.round_data(x), _tools.round_data(y), _tools.round_data(z)
        self._position = coordinate_system.Position(x, y, z)

        # Handle _position2elements
        for self_list in self.experiment._position2elements.values():
            if self in self_list:
                self_list.remove(self)

        if self._position in self.experiment._position2elements.keys():
            self.experiment._position2elements[self._position].append(self)
        else:
            self.experiment._position2elements[self._position] = [self]

        return self

    def set_rotation(
        self,
        x_r: num_type,
        y_r: num_type,
        z_r: num_type,
    ) -> Self:
        """设置元件的角度"""
        if (
            not isinstance(x_r, (int, float))
            or not isinstance(y_r, (int, float))
            or not isinstance(z_r, (int, float))
        ):
            raise TypeError

        x_r, y_r, z_r = (
            _tools.round_data(x_r),
            _tools.round_data(y_r),
            _tools.round_data(z_r),
        )
        self._rotation = coordinate_system.Rotation(x_r, y_r, z_r)
        return self
