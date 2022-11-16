from math import degrees, radians, cos, sin, atan

# given
dot = (5, -15)  # bullet position
center = (5, 5) # player position
angle = 33.69   # player angle

# calculate
x = dot[0] - center[0]
y = dot[1] - center[1]

try:
    b = degrees(atan(y / x))
except ZeroDivisionError:
    b = 90 if y > 0 else 270

new = radians(b - angle)
r = (x ** 2 + y ** 2) ** 0.5

nx, ny = r * cos(new) + center[0], r * sin(new) + center[1]

print((round(nx, 2), round(ny, 2)))

# def hitbox(bullet_dot: Dot, clone_dot: Dot, clone_angle: int, clone_size: int) -> bool:
#     # relative dot (a, b) to clone_dot as origin (0, 0)
#     a = bullet_dot.x - clone_dot.x
#     b = bullet_dot.y - clone_dot.y
#     R = sqrt(a ** 2 + b ** 2)

#     alpha = 0 if 0 in [a, b] else degrees(atan(b / a)) 
#     arg = (alpha - clone_angle + 360) % 360 # arg > 0

#     new_dot = Dot(round(R * cos(radians(arg))), round(R * sin(radians(arg))))
#     d = clone_size / 2

#     return -d <= new_dot.x <= d and -d <= new_dot.y <= d