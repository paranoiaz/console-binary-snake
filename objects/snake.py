import yaml

config = yaml.safe_load(open("config.yml", "r"))


class SnakeSprite:

    def __init__(self):
        self.x = int(config["grid_size"]/2)
        self.y = int(config["grid_size"]/2)
        self.head_position = (self.x, self.y)
        self.length = 1
        self.direction = ""

    def move_position(self):
        # keeps going in that direction without input
        if self.direction == "w":
            self.move_up()
            return
        if self.direction == "s":
            self.move_down()
            return
        if self.direction == "a":
            self.move_left()
            return
        if self.direction == "d":
            self.move_right()
            return

    def move_up(self):
        self.y -= 1
        return self.y

    def move_down(self):
        self.y += 1
        return self.y

    def move_left(self):
        self.x -= 1
        return self.x

    def move_right(self):
        self.x += 1
        return self.x