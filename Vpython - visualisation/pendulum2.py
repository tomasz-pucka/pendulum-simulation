# python 2.7
from visual import *
from visual.graph import *

PI = 3.14159265359


def acceleration(angle, velocity, gravity, length, damping):
    acceleration = -gravity / length * sin(angle) - damping * velocity
    return acceleration


def pendulum(end_time, dt, initial_angle, target_angle, accuracy, mass, length, damping, gravity):
    target_energy = mass * gravity * length * (1 - cos(target_angle))
    initial_energy = mass * gravity * length * (1 - cos(initial_angle))
    time = 0
    angle = initial_angle
    max_angle = initial_angle
    previous_angle = initial_angle
    previous_min_angle_difference = initial_angle
    if (damping != 0):
        if (abs(initial_angle) != target_angle):
            additional_velocity = sqrt((2 * (abs(target_energy - initial_energy))) / mass * (length ** 2)) / accuracy
        else:
            additional_velocity = sqrt(2 * target_energy / mass * (length ** 2)) / accuracy
    else:
        if (abs(initial_angle) < target_angle):
            additional_velocity = sqrt((2 * (abs(target_energy - initial_energy))) / mass * (length ** 2))
        else:
            additional_velocity = 0
    velocity = additional_velocity * (-1) if abs(initial_angle) > 0 else additional_velocity
    previous_velocity = velocity
    while time < end_time:
        rate(100)
        if (damping == 0 and previous_angle < 0 and angle > 0 and abs(initial_angle) > target_angle and (
                angle - previous_angle) < previous_min_angle_difference):
            previous_min_angle_difference = angle - previous_angle
            velocity = sqrt((2 * (abs(target_energy)) / mass * (length ** 2)))
        if (damping == 0 and previous_angle > 0 and angle < 0 and abs(initial_angle) > target_angle and (
                previous_angle - angle) < previous_min_angle_difference):
            previous_min_angle_difference = previous_angle - angle
            velocity = (-1) * sqrt((2 * (abs(target_energy)) / mass * (length ** 2)))

        if ((previous_velocity < 0 and velocity > 0) or (previous_velocity > 0 and velocity < 0)):
            prev_max_angle = max_angle
            max_angle = abs(angle)
        if (damping != 0 and previous_velocity < 0 and velocity > 0):  # z lewo na prawo next
            additional_velocity += additional_velocity * (1 - max_angle / target_angle) / accuracy
            velocity += additional_velocity
        if (damping != 0 and previous_velocity > 0 and velocity < 0):  # z prawo na lewo next
            additional_velocity += additional_velocity * (1 - max_angle / target_angle) / accuracy
            velocity -= additional_velocity

        previous_velocity = velocity
        velocity = velocity + acceleration(angle, velocity, gravity, length, damping) * dt
        previous_angle = angle
        angle = angle + velocity * dt
        time = time + dt

        ball.pos = (length * sin(angle), -length * cos(angle), 0)
        rod.axis = ball.pos
        theta_time_graph.plot(pos=(time, angle))
        angular_velocity_time_graph.plot(pos=(time, velocity))
        maxtheta_time.plot(pos=(time, max_angle))


end_time = 20.3  # czas zakonczenia symulacji
dt = 0.01  # krok czasowy
initial_angle = 0.4  # liczba z przedzialu (-PI, PI)
target_angle = 2  # liczba z przedzialu (0, PI)
accuracy = 3  # wprost proporcjonalne do dokladnosci wymaganego wychylenia oraz do czasu w jakim wymagane wychylenie zostanie wyregulowane; liczba z przedzialu <1;--)
# im wieksze damping lub initial_angle tym wieksze powinno byc accuracy, natomiast dt mniejsze. w innym wypadku uklad nie bedzie funkcjonowal prawidlowo
mass = 1  # masa kuli
length = 1  # dlugosc linki
damping = 3  # wspolczynnik tlumienia
gravity = 9.8  # przyspieszenie grawitacyjne

gdisplay(x=0, y=350, title='velocity(time)')
angular_velocity_time_graph = gcurve(color=color.green)
gdisplay(x=0, y=0, title='maxtheta(time)')
maxtheta_time = gcurve(color=color.red)
gdisplay(x=800, y=350, title='angle(time)')
theta_time_graph = gcurve(color=color.orange)
display(x=800, y=0)
ball = sphere(pos=(length * sin(initial_angle), -length * cos(initial_angle), 0), radius=length / 10.0)
rod = cylinder(pos=(0, 0, 0), axis=ball.pos, radius=ball.radius * 0.1)
start_rod = cylinder(pos=(0, 0, 0), axis=ball.pos, radius=ball.radius * 0.1, color=color.cyan,
                     opacity=0.25)  # beginning line.
target_rod1 = cylinder(pos=(0, 0, 0), axis=(length * sin(target_angle), -length * cos(target_angle), 0),
                       radius=ball.radius * 0.1, color=color.red, opacity=0.25)  # target angle1.
target_rod2 = cylinder(pos=(0, 0, 0), axis=(-length * sin(target_angle), -length * cos(target_angle), 0),
                       radius=ball.radius * 0.1, color=color.red, opacity=0.25)  # target angle2.

pendulum(end_time, dt, initial_angle, target_angle, accuracy, mass, length, damping, gravity)
