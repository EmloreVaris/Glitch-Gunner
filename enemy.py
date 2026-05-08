class Enemy:
    def __init__(self, eid: int) -> None:
        self.eid = eid
        self.setup()

    def setup(self):
        raise NotImplementedError("Finish Enemy setup function bozo")