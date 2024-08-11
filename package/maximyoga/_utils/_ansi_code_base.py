class ANSICodeBase:
    def __init__(self, value: int) -> None:
        self.value = f"\033[{value}m"

    def __repr__(self) -> str:
        return self.value

    def __add__(self, other) -> str:
        if isinstance(other, str):
            return f"{self.value}{other}"
        elif isinstance(other, ANSICodeBase):
            return f"{self.value}{other.value}"
        else:
            raise TypeError(f"Cannot add value of type {type(other).__name__} to an ANSI code object.")

    def __radd__(self, other) -> str:
        if isinstance(other, str):
            return f"{other}{self.value}"
        elif isinstance(other, ANSICodeBase):
            return f"{other.value}{self.value}"
        else:
            raise TypeError(f"Cannot add value of type {type(other).__name__} to an ANSI code object.")

    def __call__(self) -> None:
        print(self.value, end='')
