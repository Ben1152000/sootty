class SoottyConfig:
    def __init__(self, user_start=None, user_end=None, visible_wires=None):
        self.user_start = user_start
        self.user_end = user_end
        self.visible_wires = visible_wires if visible_wires is not None else []

    def set_user_start(self, user_start):
        self.user_start = user_start

    def set_user_end(self, user_end):
        self.user_end = user_end

    def set_visible_wires(self, visible_wires):
        self.visible_wires = visible_wires

    def get_time_window(self):
        return self.user_start, self.user_end
    
    def get_visible_wires(self):
        return self.visible_wires
