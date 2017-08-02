#head light, tail light, left right,ready, error
#LED lighting system
#number free, 7,11,12,13,15,16,18,22,29,31,32,33,35,36,37,38,40
light1 =
light2 =
light3 =
light4 =
light5 =
LED = [light1,light2,light3,light4,light5]
GPIO.setup(LED,GPIO.OUT,initial = GPIO.LOW)

def light1_on():
    GPIO.output(light1, GPIO.HIGH)


def light1_off():
    GPIO.output(light1, GPIO.LOW)


def light2_on():
    GPIO.output(light2, GPIO.HIGH)


def light2_off():
    GPIO.output(light2, GPIO.LOW)


def light3_on():
    GPIO.output(light3, GPIO.HIGH)


def light3_off():
    GPIO.output(light3, GPIO.LOW)


def light4_on():
    GPIO.output(light4, GPIO.HIGH)


def light4_off():
    GPIO.output(light4, GPIO.LOW)


def light5_on():
    GPIO.output(light5, GPIO.HIGH)


def light5_off():
    GPIO.output(light5, GPIO.LOW)

def headlight_on:
    pass


def tail_light_on:
    pass


def signal_light_left_on:
    pass


def signal_light_right_on:
    pass


def car_ready_light_on:
    pass