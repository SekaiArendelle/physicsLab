class Position:
    x: float
    y: float
    z: float

    def __init__(self, x: float, y: float, z: float) -> None:
        if not isinstance(x, float):
            raise TypeError(
                f"Parameter `x` must be of type `float`, but got value `{x}` of type `{type(x).__name__}`"
            )
        if not isinstance(y, float):
            raise TypeError(
                f"Parameter `y` must be of type `float`, but got value `{y}` of type `{type(y).__name__}`"
            )
        if not isinstance(z, float):
            raise TypeError(
                f"Parameter `z` must be of type `float`, but got value `{z}` of type `{type(z).__name__}`"
            )

        self.x = x
        self.y = y
        self.z = z

    def as_postion_str_in_plsav(self) -> str:
        return f"{self.x},{self.z},{self.y}"
