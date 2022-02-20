class concrete_item:
    """
    Concrete item implemented by whatever concrete tech is used.
    For example Qt.
    """
    def __init__(self, parent = None):
        pass

    def update_geometry(self, item) -> None:
        pass

    def set_outline(self, pen) -> None:
        pass
        
    def set_fill(self, color) -> None:
        pass

    def set_opacity(self, opacity) -> None:
        pass

    def set_shows(self, shown: bool) -> None:
        pass

    def get_shown(self) -> bool:
        return True

