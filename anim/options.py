from .named import named

class option(named):
    def __init__(self, name: str, description: str, value, low_value: None, high_value: None) -> None:
        super().__init__(name, description)
        self.value = value
        self.low_value = low_value
        self.high_value = high_value
        self.default_value = value

    def reset(self):
        self.value = self.default_value

options = list


