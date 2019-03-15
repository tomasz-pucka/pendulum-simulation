import matplotlib.pyplot as plt
from math import cos, sin, sqrt
PI=3.14159265359
def pendulum(end_time, dt, initial_angle, target_angle, accuracy, mass, length, damping, gravity):
    target_energy=mass*gravity*length*(1-cos(target_angle)) #energia potencjalna docelowa
    initial_energy=mass*gravity*length*(1-cos(initial_angle)) #energia potencjalna poczatkowa
    time=0
    angle=initial_angle
    max_angle=initial_angle
    previous_min_angle_difference=initial_angle
    previous_angle=initial_angle        #przypisanie zmiennym początkowych wartości
    if(damping!=0):
        if (abs(initial_angle)!=target_angle): additional_velocity = sqrt((2 * (abs(target_energy - initial_energy))) / mass * (length ** 2))/accuracy
        else: additional_velocity = sqrt((2 * (target_energy)) / mass * (length ** 2))
        #wzór na prędkość kątową przekształcony ze wzoru na energie kinetyczną wahadła podzielony przez współczynnik dokładności
    else:
        if(abs(initial_angle)<target_angle): additional_velocity = sqrt((2 * (abs(target_energy - initial_energy))) / mass * (length ** 2))
        #ustawienie początkowej dodatkowej prędkości przy zerowym tłumieniu, jesli poczatkowy kat jest mniejszy od kata docelowego
        else: additional_velocity=0 #jeśli kąt początkowy jest większy od kąta docelowego, to prędkość zostanie zmniejszona przy położeniu równowagi
        #jeśli kąt początkowy i docelowy są równe, to prędkośc nie jest dodawana przy zerowym tlumieniu
    velocity = additional_velocity*(-1) if abs(initial_angle)>0 else additional_velocity #ustalenie zwrotu wektora prędkości
    previous_velocity=velocity
    time_list.extend([time])
    velocity_list.extend([velocity])
    max_angle_list.extend([max_angle])
    angle_list.extend([angle])
    additional_velocity_list.extend([additional_velocity])
    while time < end_time:
        #przypadek z brakiem tłumienia
        #wyhamowanie wahadła w pozycji przybliżonej do pozycji równowagi, do prędkości wyznaczonej przy pomocy przekształconego wzoru na energię kinetyczną
        #przejscie wahadla ze strony lewej na prawą
        if(previous_angle<0 and angle>0 and damping==0 and abs(initial_angle)>target_angle and (angle-previous_angle)<previous_min_angle_difference):
            previous_min_angle_difference=angle-previous_angle
            velocity=sqrt((2 * (abs(target_energy)) / mass * (length ** 2)))
            additional_velocity=abs(velocity)
        #przejscie wahadla ze strony prawej na lewą
        if(previous_angle>0 and angle<0 and damping==0 and abs(initial_angle)>target_angle and (previous_angle-angle)<previous_min_angle_difference):
            previous_min_angle_difference=previous_angle-angle
            velocity=(-1)*sqrt((2 * (abs(target_energy)) / mass * (length ** 2)))
            additional_velocity=abs(velocity)

        #przypadek z tłumieniem
        if((previous_velocity < 0 and velocity > 0) or (previous_velocity > 0 and velocity < 0)): #moment maksymalnego wychylenia
            max_angle=abs(angle)
        if (previous_velocity < 0 and velocity > 0 and damping!=0): #moment maksymalnego wychylenia po lewej stronie
            additional_velocity += additional_velocity * (1 - max_angle / target_angle)/accuracy
            #dodawanie coraz mniejszych wartości wraz ze zbliżaniem się do docelowego wychylenia
            velocity+=additional_velocity
        if (previous_velocity > 0 and velocity < 0 and damping!=0): #moment maksymalnego wychylenia po prawej stronie
            additional_velocity += additional_velocity * (1 - max_angle / target_angle)/accuracy
            velocity -= additional_velocity

        previous_velocity = velocity
        velocity = velocity + (-gravity/length*sin(angle)-damping*velocity) * dt
        previous_angle=angle
        angle = angle + velocity * dt
        time = time + dt

        time_list.extend([time])
        velocity_list.extend([velocity])
        max_angle_list.extend([max_angle])
        angle_list.extend([angle])
        additional_velocity_list.extend([additional_velocity])

#parametry wejściowe
end_time        = 25    # czas zakonczenia symulacji
dt              = 0.01  # krok czasowy. sugerowana liczba z przedzialu: (0;0.3)
initial_angle   = 1     # liczba z przedzialu (-PI, PI) [radians]
target_angle    = 2     # liczba z przedzialu (0, PI) [radians]

damping         = 1     # wspolczynnik tlumienia (zakłócenie). sugerowana liczba z przedzialu: <0;7)
                        # jesli damping==0, accuracy nie ma znaczenia.

accuracy        = 1     # współczynnik dokładności, liczba z przedzialu <1;--). sugerowana liczba z przedzialu: <1;25>
                        # wprost proporcjonalne do dokladnosci wymaganego wychylenia oraz do czasu w jakim oczekiwane wychylenie zostanie wyregulowane.
                        # im wieksze damping lub initial_angle tym wieksze powinno byc accuracy, natomiast dt mniejsze.
                        # w innym wypadku uklad nie bedzie funkcjonowal prawidlowo

mass            = 1   # masa ciała
length          = 1     # dlugosc nici. sugerowana wartosc dla poprawnego dzialania ukladu: 1.
gravity         = 10   # przyspieszenie grawitacyjne

time_list=[]
velocity_list=[]
max_angle_list=[]
angle_list=[]
additional_velocity_list=[]

#główna funkcja
pendulum(end_time, dt, initial_angle, target_angle, accuracy, mass, length, damping, gravity)
#tworzenie wykresów
plt.subplot(2, 2, 1)
plt.plot(time_list, angle_list)
target_angle_plot,=plt.plot(time_list, [target_angle]*len(time_list), color='red')
plt.plot(time_list, [-target_angle]*len(time_list), color='red')
plt.title('Kąt między wahadłem a położeniem równowagi w czasie', weight='bold')
plt.ylabel('Kąt wychylenia[radian]')
plt.xlabel('Czas')
plt.legend([target_angle_plot],['Docelowy kąt wychylenia'])

plt.subplot(2, 2, 2)
plt.plot(time_list, velocity_list)
plt.title('Prędkość kątowa wahadła w czasie (wielkość regulowana)', weight='bold')
plt.ylabel('Prędkość kątowa')
plt.xlabel('Czas')

plt.subplot(2, 2, 3)
plt.plot(time_list, max_angle_list, '.', markersize='0.5')
target_max_angle_plot,=plt.plot(time_list, [target_angle]*len(time_list), color='red')
plt.title('Wartość bezwzględna kątów maksymalnych wychyleń w czasie', weight='bold')
plt.ylabel('Kąt wychylenia[radian]')
plt.xlabel('Czas')
plt.legend([target_max_angle_plot],['Docelowy kąt wychylenia'])
if(damping==0 and initial_angle==target_angle): plt.axis([0, end_time, initial_angle, target_angle])

plt.subplot(2, 2, 4)
plt.plot(time_list, additional_velocity_list, '.', markersize='0.5')
plt.title('Dodatkowa szybkość kątowa wahadła w czasie (wielkość sterująca)', weight='bold')
plt.ylabel('Szybkość kątowa')
plt.xlabel('Czas')

plt.subplots_adjust(left=0.06, bottom=0.08, right=0.97, top=0.94, wspace=0.14, hspace=0.30)
plt.show()