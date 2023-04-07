import sys

from flask import Flask, request

from yeelight import Bulb, Flow
from yeelight.flow import Action, HSVTransition

# bulb temp = 2884 (technically 3000)
default_bulb_temp = 3800

test_bulb = Bulb("192.168.0.224")
bulb1 = Bulb("192.168.0.86")
bulb2 = Bulb("192.168.0.77")
bulb3 = Bulb("192.168.0.101")
bulb4 = Bulb("192.168.0.245")
bulb1_brightness = None
bulb2_brightness = None
bulb3_brightness = None
bulb4_brightness = None

colors = {
    "red": (255, 0, 0),
    "orange":(255, 110, 0),
    "yellow":(255, 200, 0),
    "green":(0, 255, 0),
    "skyblue":(0, 255, 255),
    "blue":(0, 0, 255),
    "purple":(128, 0, 255),
    "pink":(255, 0, 255)
}

app = Flask(__name__)

@app.route('/bulb1', methods=['GET'])
def result():
    color = request.args.get("color")
    toggle = request.args.get("toggle")
    brightness = request.args.get("brightness")

    print("Bulb: 1\nColor: {}\nToggle: {}\nBrightness: {}".format(color, toggle, brightness), file=sys.stderr)

    global bulb1_brightness
    if brightness is not None:
        if bulb1_brightness is None:
            bulb1_brightness = int(bulb1.get_properties()["bright"])
    set_bulb(bulb1, color, 1, bulb1_brightness, brightness, toggle)
    return("Received")

@app.route('/bulb2', methods=['GET'])
def second_bulb():
    color = request.args.get("color")
    toggle = request.args.get("toggle")
    brightness = request.args.get("brightness")

    print("Bulb: 2\nColor: {}\nToggle: {}\nBrightness: {}".format(color, toggle, brightness), file=sys.stderr)

    global bulb2_brightness
    if brightness is not None:
        if bulb2_brightness is None:
            bulb2_brightness = int(bulb2.get_properties()["bright"])
    set_bulb(bulb2, color, 2, bulb2_brightness, brightness, toggle)
    return("Received")

@app.route('/bulb3', methods=['GET'])
def third_bulb():
    color = request.args.get("color")
    toggle = request.args.get("toggle")
    brightness = request.args.get("brightness")

    print("Bulb: 3\nColor: {}\nToggle: {}\nBrightness: {}".format(color, toggle, brightness), file=sys.stderr)

    global bulb3_brightness
    if brightness is not None:
        if bulb3_brightness is None:
            bulb3_brightness = int(bulb3.get_properties()["bright"])
    set_bulb(bulb3, color, 3, bulb3_brightness, brightness, toggle)
    return("Received")

@app.route('/bulb4', methods=['GET'])
def fourth_bulb():
    color = request.args.get("color")
    toggle = request.args.get("toggle")
    brightness = request.args.get("brightness")

    print("Bulb: 4\nColor: {}\nToggle: {}\nBrightness: {}".format(color, toggle, brightness), file=sys.stderr)

    global bulb4_brightness
    if brightness is not None:
        if bulb4_brightness is None:
            bulb4_brightness = int(bulb4.get_properties()["bright"])
    set_bulb(bulb4, color, 4, bulb4_brightness, brightness, toggle)
    return("Received")

@app.route('/all', methods=['GET'])
def allbulbs():
    color = request.args.get("color")
    toggle = request.args.get("toggle")
    brightness = request.args.get("brightness")

    print("Bulbs: All\nColor: {}\nToggle: {}\nBrightness: {}".format(color, toggle, brightness), file=sys.stderr)

    if brightness is not None:
        global bulb1_brightness
        global bulb2_brightness
        global bulb3_brightness
        global bulb4_brightness
        if bulb1_brightness is None:
            bulb1_brightness = int(bulb1.get_properties()["bright"])
        if bulb2_brightness is None:
            bulb2_brightness = int(bulb2.get_properties()["bright"])
        if bulb3_brightness is None:
            bulb3_brightness = int(bulb3.get_properties()["bright"])
        if bulb4_brightness is None:
            bulb4_brightness = int(bulb4.get_properties()["bright"])

    set_bulb(bulb1, color, 1, bulb1_brightness, brightness, toggle)
    set_bulb(bulb2, color, 2, bulb2_brightness, brightness, toggle)
    set_bulb(bulb3, color, 3, bulb3_brightness, brightness, toggle)
    set_bulb(bulb4, color, 4, bulb4_brightness, brightness, toggle)

    return("Received")


def set_bulb(bulb, color, bulb_id, old_brightness, brightness, toggle):
    if toggle is not None:
        if toggle == "on":
            bulb.turn_on()
        else:
            bulb.turn_off()
    if color is not None:
        if color == "white":
            bulb.set_color_temp(5000)
        elif color == "default":
            bulb.set_color_temp(default_bulb_temp)
        elif color == "rainbow":
            bulb.start_flow(Flow(count=0, action=Action.stay, transitions=rainbow()))
        else:
            bulb.set_rgb(colors[color][0], colors[color][1], colors[color][2])
    if brightness is not None:
        new_brightness = old_brightness
        if brightness.startswith("-"):
            new_brightness -= int(brightness.split("-")[1])
            if new_brightness < 0:
                bulb_brightness = 0

        elif brightness.startswith("+"):
            new_brightness += int(brightness.split("+")[1])
            if new_brightness > 100:
                new_brightness = 100
        else:
            new_brightness = int(brightness)

        bulb.set_brightness(new_brightness)
        if bulb_id == 1:
            global bulb1_brightness
            bulb1_brightness = new_brightness
        elif bulb_id == 2:
            global bulb2_brightness
            bulb2_brightness = new_brightness
        elif bulb_id == 3:
            global bulb3_brightness
            bulb3_brightness = new_brightness
        elif bulb_id == 4:
            global bulb4_brightness
            bulb4_brightness = new_brightness

def rainbow(duration=3000, brightness=100):
    h_values = [0, 20, 40, 120, 140, 180, 230, 260]
    return [HSVTransition(hue, 100, duration=duration, brightness=brightness) for hue in h_values]

