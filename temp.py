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