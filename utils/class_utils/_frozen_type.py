class _FrozenType(type):
    """Metaclass that freezes attributes and blocks reassignment."""

    def __setattr__(cls, name, value):
        raise AttributeError(f"{cls.__name__} is frozen. Cannot modify '{name}'.")

    def __call__(cls, *args, **kwargs):
        raise TypeError(f"{cls.__name__} is not meant to be instantiated.")
