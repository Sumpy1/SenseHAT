#Written by Gopal(Sumiran Pokharel) for collecting acceleration and orientation values from a Sense HAT connected to a raspberry pi
#Used complimentary filter to remove gravity component from accelerometer data
from sense_hat import SenseHat
import time
import os
sense= SenseHat() 
#Enables and disables the magnetometer, gyroscope and/or accelerometer contribution to the get orientation functions below.
sense.set_imu_config(False, True, False)


labels = {
    "timestamp": "Timestamp",
    "accel_x": "Acceleration X",
    "accel_y": "Acceleration Y",
    "accel_z": "Acceleration Z",
    "orientation_pitch": "Orientation Pitch",
    "orientation_roll": "Orientation Roll",
    "orientation_yaw": "Orientation Yaw"
}

def collect_data(duration):
    start_time = time.time()
    end_time = start_time + duration

    data = []  # List to store the collected data

    while time.time() < end_time:
        accelerometer_raw = sense.get_accelerometer_raw()
        orientation_degrees = sense.get_orientation_degrees()
        orientation_radians = sense.get_orientation_radians()

        data.append({
            'timestamp': time.time()-start_time,
            'accel_x': accelerometer_raw['x']-(0.98 * orientation_radians['pitch']), 
            'accel_y': accelerometer_raw['y']-(0.98 * orientation_radians['roll']),
            'accel_z': accelerometer_raw['z']-(0.98 * orientation_radians['yaw']),
            'orientation_pitch': orientation_degrees['pitch'], #simply change the "degrees" to radians if you want the orientation in radian
            'orientation_roll': orientation_degrees['roll'],
            'orientation_yaw': orientation_degrees['yaw']
        })

        time.sleep(0.1) # Delay between readings (adjust as needed)
       
    return data


def save_data_to_file(data, filename):
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    file_path = os.path.join(desktop_path, filename)  
#file_path = "/home/pi/Desktop/data.txt"
# Example file path, replace with your desired file path

    with open(file_path, 'w') as file:
        header = ", ".join(labels.values())
        file.write(header + "\n")
        for item in data:
            data_row = ", ".join([f"{item[key]:.2f}" for key in labels.keys()])
            file.write(data_row + "\n")

    print(f"Data saved to: {file_path}")

# Set the duration for data collection (in seconds)
duration = 5

# Collect accelerometer and orientation data
data = collect_data(duration)

# Save the collected data to a file on the Desktop
save_data_to_file(data, 'data_woG1.csv')

