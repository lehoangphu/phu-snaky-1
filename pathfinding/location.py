class Location:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
    def __repr__(self) -> str:
        retString = "(" + str(self.x) + ", " + str(self.y) + ")"
        return retString
    def __eq__(self, object) -> bool:
        if self.x == object.x and self.y == object.y:
            return True
        else:
            return False
    def __hash__(self):
        return self.x*1000 + self.y
    def get_distance(self, location):
        return abs(self.x - location.x) + abs(self.y - location.y)