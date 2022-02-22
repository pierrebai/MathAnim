from .named import named

class option(named):
    """
    Animation option, let the user control different aspects of an animation.
    """
    def __init__(self, name: str, description: str, value, low_value = None, high_value = None) -> None:
        """
        Creates a named option, with a value and optional low and high limits.
        The value is also the default value.

        For an option to select an item from a list of strings,
        the low_value contains the list of strings.
        """
        super().__init__(name, description)
        self.value = value
        self.low_value = low_value
        self.high_value = high_value
        self.default_value = value

    def reset(self):
        """
        Resets the option to its default value.
        """
        self.value = self.default_value

options = list


