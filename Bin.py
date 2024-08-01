# Welcome to The Bin! 🦝

<!-- Now that you've thrown some parts into The Bin, it's time to turn that trash into treasure! 🗑️➡️💎

Wire up your parts and write some code to make them work together. If you need
help with a part, click the "?" above it.

If you want to see examples, check here:
https://hack.club/bin-example

You can get help by chatting with other high schoolers on the Hack Club Slack in
the #electronics channel:
👉 https://hackclub.com/slack 👈

Once you're ready build your design IRL, click the "Share" button and submit
your design:
https://hack.club/bin-submit -->

import RPi.GPIO as GPIO
import time
import pigpio


GPIO.setmode(GPIO.BCM)


#define ENCODER_CLK = 17
#define ENCODER_DT = 27
#define ENCODER_SW = 22
#define LED_R = 18
#define LED_G = 23
#define LED_B = 24
#define SERVO_PIN = 25


GPIO.setup(ENCODER_CLK, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(ENCODER_DT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(ENCODER_SW, GPIO.IN, pull_up_down=GPIO.PUD_UP)


pi = pigpio.pi()

r_duty = 0
g_duty = 0
b_duty = 0


servo = pi.set_servo_pulsewidth(SERVO_PIN, 1500)  # 1500µs for middle position


last_clk = GPIO.input(ENCODER_CLK)
color_value = 0
servo_position = 1500  # 1500µs (center position)
increment = 100  # Pulse increment for servo movement

def set_color(value):
    """ Set the RGB LED color based on value. """
    value = value % 255
    if value < 85:
        r = value * 3
        g = 255 - value * 3
        b = 0
    elif value < 170:
        value -= 85
        r = 255 - value * 3
        g = 0
        b = value * 3
    else:
        value -= 170
        r = 0
        g = value * 3
        b = 255 - value * 3

    pi.set_PWM_dutycycle(LED_R, r)
    pi.set_PWM_dutycycle(LED_G, g)
    pi.set_PWM_dutycycle(LED_B, b)

def move_servo(position):
    """ Move servo to position (500 to 2500µs). """
    pi.set_servo_pulsewidth(SERVO_PIN, position)

try:
    while True:
        current_clk = GPIO.input(ENCODER_CLK)
        if current_clk != last_clk:
            if GPIO.input(ENCODER_DT) != current_clk:
                color_value += 1
            else:
                color_value -= 1
            set_color(color_value)
        last_clk = current_clk

        if GPIO.input(ENCODER_SW) == GPIO.LOW:  # Button pressed
            servo_position = (servo_position + increment) % 2500
            if servo_position < 500:
                servo_position = 500
            move_servo(servo_position)
            time.sleep(0.2)  # Debounce delay

        time.sleep(0.01)  # Small delay to avoid excessive CPU usage

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()
    pi.stop()
