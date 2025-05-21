

def update_input(dt, keyboard, player, gravity, clock):
    dt = clock.tick() / 1000  # Convert milliseconds to seconds
    movement_speed = 600
    print(gravity.vertical_velocity)
    if keyboard.up or keyboard.w and gravity.vertical_velocity == 0:
        gravity.jump(dt)
    if keyboard.left or keyboard.a:
        player.x_change -= movement_speed * dt
    if keyboard.right or keyboard.d:
        player.x_change += movement_speed * dt
    gravity.apply_gravity(dt)