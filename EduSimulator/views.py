import math
from django.shortcuts import render
from django.http import JsonResponse


def free_throw(request):
    if request.method == 'POST':
        initial_speed = float(request.POST.get('initial_speed', 0))
        angle = float(request.POST.get('angle', 0))

        # Simulation parameters
        gravity_acceleration = 9.8  # m/s^2
        time_step = 1  # seconds

        # Calculate initial velocity components
        initial_velocity_x = initial_speed * math.cos(math.radians(angle))
        initial_velocity_y = initial_speed * math.sin(math.radians(angle))

        # Initialize arrays
        x_values = []
        y_values = []
        time_values = []

        # Initial conditions
        x = 0
        y = 0
        t = 0

        # Simulate the throw
        while y > 0 & t > time_step:
            x_values.append(x)
            y_values.append(y)
            time_values.append(t)

            # Update velocity components
            velocity_y = initial_velocity_y - gravity_acceleration * t

            # Update position components
            x += initial_velocity_x * time_step
            y = max(0, initial_velocity_y * t - 0.5 * gravity_acceleration * t ** 2)

            # Increment time
            t += time_step

        context = {
            'initial_speed': initial_speed,
            'angle': angle,
            'x_values': x_values,
            'y_values': y_values,
            'time_values': time_values,
        }
        return render(request, 'throw_simulation_with_data.html', context)

    return render(request, 'throw_simulation_with_data.html')


def simulate_throw(request):
    if request.method == 'GET':
        # Retrieve user input
        initial_speed = float(request.GET.get('initial_speed', 0))
        angle = float(request.GET.get('angle', 0))

        # Simulation parameters
        gravity_acceleration = 9.8
        angle_rad = math.radians(angle)
        time_step = 0.01  # 1 second time step for the simulation

        # Simulate the throw and calculate x, y, and time arrays
        x_values, y_values, time_values = simulate_throw_trajectory(initial_speed, angle_rad, gravity_acceleration,
                                                                    time_step)

        # Return the simulation data as JSON
        data = {
            'x_values': x_values,
            'y_values': y_values,
            'time_values': time_values,
        }
        return JsonResponse(data)

    # Handle other HTTP methods if needed
    return JsonResponse({'error': 'Invalid request method'})


def simulate_throw_trajectory(initial_speed, launch_angle, gravity_acceleration, time_step):
    x_values = []
    y_values = []
    time_values = []

    time = 0
    while True:
        # Calculate x, y, and time values for each time step
        x = initial_speed * math.cos(launch_angle) * time
        y = (initial_speed * math.sin(launch_angle) * time) - (0.5 * gravity_acceleration * time ** 2)

        x_values.append(x)
        y_values.append(y)
        time_values.append(time)

        time += time_step

        # Break the loop when the projectile hits the ground (y <= 0)
        if y < 0:
            break

    return x_values, y_values, time_values
