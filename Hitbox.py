from Entity import Entity


GRAVITY = 9.8  # m/s^2, adjust as needed for your game's scale

class Hitbox(Entity):
    def __init__(self, x, y, width, height, type, mass=1.0, friction_coefficient=0.5):
        super().__init__(x, y, width, height, type)
        self.x_vel = 0
        self.y_vel = 0
        self.mass = mass
        self.friction_coefficient = friction_coefficient
        self.grounded = True  # Add a grounded state

    def friction(self):
        if self.x_vel > 0:
            self.x_vel -= self.friction_coefficient
        elif self.x_vel < 0:
            self.x_vel += self.friction_coefficient


    def update(self, dt):
        self.friction()
        self.x += self.x_vel
        self.y += self.y_vel