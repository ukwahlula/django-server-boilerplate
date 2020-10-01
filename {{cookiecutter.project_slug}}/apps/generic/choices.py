class BaseChoices:
    @classmethod
    def choices(cls):
        return [(f, f) for f in dir(cls) if not callable(getattr(cls, f)) and not f.startswith("__")]

    @classmethod
    def has_choice(cls, choice):
        return choice in [f for f in dir(cls) if not callable(getattr(cls, f)) and not f.startswith("__")]
