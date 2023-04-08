from operator import truediv
from pickle import TRUE
import serial
import RPi.GPIO as GPIO
import time  # import the PySerial library

#custom libs
from detect import detect

GPIO.setmode(GPIO.BOARD)
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=0.1)  # open the serial port at 9600 baud

#motor setup
servo_pin = 12
GPIO.setup(servo_pin, GPIO.OUT)
pwm = GPIO.PWM(servo_pin, 50)
time.sleep(1)
pwm.start(2.5)
time.sleep(1)

#buzzer/speaker setup
buzzer_pin = 23
GPIO.setup(buzzer_pin, GPIO.OUT)

#arduino outputs
temp = ""

#close servp
isClosed = True
print("Close servo")

start = time.time()
alcohol_tested = False
min_time = 20 #alcohol window

#eye tracker
eye_detect = detect()
state = 0

#initial questions
isAsked = False
isPassed = True
isRunning = True
lastValue = 0
isSendReceived = False

while isRunning:
	state = eye_detect.getState()
	#print("rpi.py view state: ", state)
	data = ser.read()  # read a single byte of data from the Arduino
	ch = ""
	#print(data)
	try:
		ch = data.decode('utf-8')
	except:
		time.sleep(0)
	#print(data,ch)
	#check
	letters = (ch >= 'a' and ch <= 'z') or (ch >= 'A' and ch <= 'Z')
	nums = ch >= '0' and ch <= '9'
	reserve = ch == ' ' or ch == '\r' or ch == '\n' or ch == '-'
	start_time = 0

	#letters = True
	if nums or letters or reserve: #arduino input
		if ch == '\n':
			print("Arduino callback: " + temp)
			temp = ""
		elif ch == '\r':
			temp += ""
		else:
			temp += ch

		if not isAsked: #such that within time limit
			isAsked = True
			while time.time()-start < min_time:
				try:
					value = int("0"+temp)
					if value >= 450:
						isPassed = False
					else:
						isPassed = True
				except:
					if temp == "emergency":
						print("Emergency mode!!!")
						if isClosed:
							pwm.ChangeDutyCycle(7) #assumes as open
							isClosed = False
						if eye_detect.isRunning() and not isSendReceived: #if running and not yet sendrcv
							isSendReceived = True
							buff = str(-2)+"\n"
							ser.flush()
							print(buff)
							ser.write(buff.encode())
							print("Stopping alcohol detect...")
						elif not eye_detect.isRunning() and state != -1:
							print("Running camera...")
							eye_detect.run()
						state = eye_detect.getState()
						if state != lastValue:
							print("Change value: ", lastValue, " > ", state)
							lastValue = state
							buff = str(state)+"\n"
							ser.flush()
							ser.write(buff.encode())
							'''GPIO.setup(buzzer_pin, GPIO.HIGH)
							time.sleep(1)
							GPIO.setup(buzzer_pin, GPIO.LOW)'''
						print("State: ", state)
						if state == -1:
							isRunning = False
		else: #natanong na kung lasing o hindi
			if isAsked and isPassed:
				if isClosed:
					pwm.ChangeDutyCycle(7) #assumes as open
					isClosed = False
				if eye_detect.isRunning() and not isSendReceived: #if running and not yet sendrcv
					isSendReceived = True
					buff = str(-2)+"\n"
					ser.flush()
					ser.write(buff.encode())
					print("Stopping alcohol detect...")
				if not eye_detect.isRunning() and state != -1:
					print("Running camera...")
					eye_detect.run()
				state = int(eye_detect.getState())
				if state != lastValue:
					print("Change value: ", lastValue, " > ", state)
					lastValue = state
					buff = str(state)+"\n"
					ser.flush()
					print(buff)
					ser.write(buff.encode())
					'''GPIO.setup(buzzer_pin, GPIO.HIGH)
					time.sleep(1)
					GPIO.setup(buzzer_pin, GPIO.LOW)'''
				if state == -1:
					isRunning = False
				print("Blink_State: ", state)
				if state != -1: #Call 'detect.stop_eye()' for code equivalent
					buff = str(state)+"\n"
					ser.flush()
					ser.write(buff.encode())
				else:
					temp_state = 6
					ser.write(temp_state.to_bytes(1,'big'))
print("Servo reset")
pwm.ChangeDutyCycle(2.5)
#never lumabas ng loop
