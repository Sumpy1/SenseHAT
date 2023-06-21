from sense_hat import SenseHat

sense = SenseHat()
sense.set_imu_config(True,True,False)
while True:
    orientation = sense.get_orientation()
    print("p: {pitch:.2f}, r: {roll:.2f}, y: {yaw:.2f}".format(**orientation))