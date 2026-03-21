import json
from physicsLab._typing import List
from . import _base

class StatusSave:
    __elements: List[_base.ElectromagnetismBase]

    def __init__(self) -> None:
        self.__elements = []

    @property
    def elements(self) -> List[_base.ElectromagnetismBase]:
        return self.__elements

    def append_element(self, element: _base.ElectromagnetismBase) -> None:
        if not isinstance(element, _base.ElectromagnetismBase):
            raise TypeError(
                f"parameter element must be of type `ElectromagnetismBase`, but got value {element} of type {type(element).__name__}"
            )
        self.__elements.append(element)

    def as_dict(self) -> dict:
        return {
            "SimulationSpeed": 1.0,
            "Elements": [element.as_dict() for element in self.elements],
        }

    def as_str_in_plsav(self) -> str:
        return json.dumps(self.as_dict())
