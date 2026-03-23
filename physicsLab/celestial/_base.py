import abc
from physicsLab import coordinate_system
from . import triple_vector


class CelestialBase:
    """Base class for celestial elements"""

    __position: coordinate_system.Position
    __velocity: triple_vector.Velocity
    __acceleration: triple_vector.Acceleration
    __identifier: str

    def __init__(
        self,
        position: coordinate_system.Position,
        velocity: triple_vector.Velocity,
        acceleration: triple_vector.Acceleration,
        identifier: str,
    ) -> None:
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration
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
    def velocity(self) -> triple_vector.Velocity:
        return self.__velocity

    @velocity.setter
    def velocity(self, velocity: triple_vector.Velocity) -> None:
        if not isinstance(velocity, triple_vector.Velocity):
            raise TypeError(
                f"velocity must be of type `Velocity`, but got value {velocity} of type {type(velocity).__name__}"
            )

        self.__velocity = velocity

    @property
    def acceleration(self) -> triple_vector.Acceleration:
        return self.__acceleration

    @acceleration.setter
    def acceleration(self, acceleration: triple_vector.Acceleration) -> None:
        if not isinstance(acceleration, triple_vector.Acceleration):
            raise TypeError(
                f"acceleration must be of type `Acceleration`, but got value {acceleration} of type {type(acceleration).__name__}"
            )

        self.__acceleration = acceleration

    @abc.abstractmethod
    def as_dict(self) -> dict:
        raise NotImplementedError(
            "The method `as_dict` must be implemented in the subclass"
        )
