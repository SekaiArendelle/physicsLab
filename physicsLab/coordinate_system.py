from ._typing import num_type


class Position:
    x: num_type
    y: num_type
    z: num_type

    def __init__(self, x: num_type, y: num_type, z: num_type) -> None:
        if not isinstance(x, (int, float)):
            raise TypeError(
                f"Parameter `x` must be of type `int | float`, but got value `{x}` of type `{type(x).__name__}`"
            )
        if not isinstance(y, (int, float)):
            raise TypeError(
                f"Parameter `y` must be of type `int | float`, but got value `{y}` of type `{type(y).__name__}`"
            )
        if not isinstance(z, (int, float)):
            raise TypeError(
                f"Parameter `z` must be of type `int | float`, but got value `{z}` of type `{type(z).__name__}`"
            )

        self.x: num_type = x
        self.y: num_type = y
        self.z: num_type = z

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.z))

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Position):
            return False

        return self.x == value.x and self.y == value.y and self.z == value.z

    def as_postion_str_in_plsav(self) -> str:
        return f"{self.x},{self.z},{self.y}"


def construct_position_from_plsav_str(position_str: str) -> Position:
    try:
        x_str, z_str, y_str = position_str.split(",")
        x = float(x_str)
        y = float(y_str)
        z = float(z_str)
        return Position(x, y, z)
    except Exception as e:
        raise ValueError(
            f"Failed to parse position string `{position_str}` in plsav format. Expected format: `x,z,y` where x, y, z are numbers. Error: {e}"
        )


class Rotation:
    x: num_type
    y: num_type
    z: num_type

    def __init__(self, x: num_type, y: num_type, z: num_type) -> None:
        if not isinstance(x, (int, float)):
            raise TypeError(
                f"Parameter `x` must be of type `int | float`, but got value `{x}` of type `{type(x).__name__}`"
            )
        if not isinstance(y, (int, float)):
            raise TypeError(
                f"Parameter `y` must be of type `int | float`, but got value `{y}` of type `{type(y).__name__}`"
            )
        if not isinstance(z, (int, float)):
            raise TypeError(
                f"Parameter `z` must be of type `int | float`, but got value `{z}` of type `{type(z).__name__}`"
            )

        self.x: num_type = x
        self.y: num_type = y
        self.z: num_type = z

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.z))

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Rotation):
            return False

        return self.x == value.x and self.y == value.y and self.z == value.z

    def as_rotation_str_in_plsav(self) -> str:
        return f"{self.x},{self.z},{self.y}"


def construct_rotation_from_plsav_str(rotation_str: str) -> Rotation:
    try:
        x_str, z_str, y_str = rotation_str.split(",")
        x = float(x_str)
        y = float(y_str)
        z = float(z_str)
        return Rotation(x, y, z)
    except Exception as e:
        raise ValueError(
            f"Failed to parse rotation string `{rotation_str}` in plsav format. Expected format: `x,z,y` where x, y, z are numbers. Error: {e}"
        )


class Velocity:
    x: num_type
    y: num_type
    z: num_type

    def __init__(self, x: num_type, y: num_type, z: num_type) -> None:
        if not isinstance(x, (int, float)):
            raise TypeError(
                f"Parameter `x` must be of type `int | float`, but got value `{x}` of type `{type(x).__name__}`"
            )
        if not isinstance(y, (int, float)):
            raise TypeError(
                f"Parameter `y` must be of type `int | float`, but got value `{y}` of type `{type(y).__name__}`"
            )
        if not isinstance(z, (int, float)):
            raise TypeError(
                f"Parameter `z` must be of type `int | float`, but got value `{z}` of type `{type(z).__name__}`"
            )

        self.x: num_type = x
        self.y: num_type = y
        self.z: num_type = z

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.z))

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Velocity):
            return False

        return self.x == value.x and self.y == value.y and self.z == value.z

    def as_velocity_str_in_plsav(self) -> str:
        return f"{self.x},{self.z},{self.y}"


def construct_velocity_from_plsav_str(velocity_str: str) -> Velocity:
    try:
        x_str, z_str, y_str = velocity_str.split(",")
        x = float(x_str)
        y = float(y_str)
        z = float(z_str)
        return Velocity(x, y, z)
    except Exception as e:
        raise ValueError(
            f"Failed to parse velocity string `{velocity_str}` in plsav format. Expected format: `x,z,y` where x, y, z are numbers. Error: {e}"
        )


class AngularVelocity:
    x: num_type
    y: num_type
    z: num_type

    def __init__(self, x: num_type, y: num_type, z: num_type) -> None:
        if not isinstance(x, (int, float)):
            raise TypeError(
                f"Parameter `x` must be of type `int | float`, but got value `{x}` of type `{type(x).__name__}`"
            )
        if not isinstance(y, (int, float)):
            raise TypeError(
                f"Parameter `y` must be of type `int | float`, but got value `{y}` of type `{type(y).__name__}`"
            )
        if not isinstance(z, (int, float)):
            raise TypeError(
                f"Parameter `z` must be of type `int | float`, but got value `{z}` of type `{type(z).__name__}`"
            )

        self.x: num_type = x
        self.y: num_type = y
        self.z: num_type = z

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.z))

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, AngularVelocity):
            return False

        return self.x == value.x and self.y == value.y and self.z == value.z

    def as_angular_velocity_str_in_plsav(self) -> str:
        return f"{self.x},{self.z},{self.y}"


def construct_angular_velocity_from_plsav_str(angular_velocity_str: str) -> AngularVelocity:
    try:
        x_str, z_str, y_str = angular_velocity_str.split(",")
        x = float(x_str)
        y = float(y_str)
        z = float(z_str)
        return AngularVelocity(x, y, z)
    except Exception as e:
        raise ValueError(
            f"Failed to parse angular velocity string `{angular_velocity_str}` in plsav format. Expected format: `x,z,y` where x, y, z are numbers. Error: {e}"
        )


class Acceleration:
    x: num_type
    y: num_type
    z: num_type

    def __init__(self, x: num_type, y: num_type, z: num_type) -> None:
        if not isinstance(x, (int, float)):
            raise TypeError(
                f"Parameter `x` must be of type `int | float`, but got value `{x}` of type `{type(x).__name__}`"
            )
        if not isinstance(y, (int, float)):
            raise TypeError(
                f"Parameter `y` must be of type `int | float`, but got value `{y}` of type `{type(y).__name__}`"
            )
        if not isinstance(z, (int, float)):
            raise TypeError(
                f"Parameter `z` must be of type `int | float`, but got value `{z}` of type `{type(z).__name__}`"
            )

        self.x: num_type = x
        self.y: num_type = y
        self.z: num_type = z

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.z))

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Acceleration):
            return False

        return self.x == value.x and self.y == value.y and self.z == value.z

    def as_acceleration_str_in_plsav(self) -> str:
        return f"{self.x},{self.z},{self.y}"


def construct_acceleration_from_plsav_str(acceleration_str: str) -> Acceleration:
    try:
        x_str, z_str, y_str = acceleration_str.split(",")
        x = float(x_str)
        y = float(y_str)
        z = float(z_str)
        return Acceleration(x, y, z)
    except Exception as e:
        raise ValueError(
            f"Failed to parse acceleration string `{acceleration_str}` in plsav format. Expected format: `x,z,y` where x, y, z are numbers. Error: {e}"
        )
