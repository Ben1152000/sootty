class SoottyConfig:
    def __init__(self, user_start=None, user_end=None):
        self.user_start = user_start
        self.user_end = user_end

    def set_user_start(self, user_start):
        self.user_start = user_start

    def set_user_end(self, user_end):
        self.user_end = user_end

    def get_time_window(self):
        return self.user_start, self.user_end
