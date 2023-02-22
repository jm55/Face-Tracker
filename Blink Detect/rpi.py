import serial
#import RPi.GPIO as GPIO
import time  # import the PySerial library

#custom libs
from detect import detect

#GPIO.setmode(GPIO.BOARD)
#ser = serial.Serial('/dev/ttyACM0', 9600, timeout=0.1)  # open the serial port at 9600 baud
servo_pin = 12
#GPIO.setup(servo_pin, GPIO.OUT)
#pwm = GPIO.PWM(servo_pin, 50)
time.sleep(1)
#pwm.start(2.5)
time.sleep(1)
temp = ""

isClosed = False
isClosed = True
print("Close servo")

start = time.time()
alcohol_tested = False
min_time = 3

#Loading eye tracker regardless
eye_detect = detect()
#eye_detect.run()

state = 0
while True:
	#state = eye_detect.getState()
	#print("State: ", state)
	data = "A" #TEMPORARY REPLACEMENT WHILE TESTING THREADING
	#data = ser.read()  # read a single byte of data from the Arduino
	ch = ""
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
	letters = True
	if nums or letters or reserve:
		if ch == '\n':
			print(temp)
			temp = ""
		elif ch == '\r':
			temp += ""
		else:
			temp += ch
		try: #nos. only
			value = int("0"+temp)
			value = 0
			#print(value)
			if time.time()-start > min_time and not alcohol_tested:
				alcohol_tested = True
				print("Within " + str(min_time) + "s...")
				print("Alcohol limit: ", value)
				if value >= 450:  #Check if more than alcohol limit
					print("Alcohol limit reached!")
					#ser.write(b'2')
				else: #Alcohol levels within acceptable range, thus open
					print("Acceptable alcohol range...")
					#pwm.ChangeDutyCycle(7) #assumes as open
					time.sleep(1)
					if not eye_detect.isRunning():
						eye_detect.run()
					state = eye_detect.getState()
					if state == 0 or state == -1: # press q
						#pwm.ChangeDutyCycle(2.5)
						time.sleep(1)
			else: #insert serial related code here
				time.sleep(0)
				#ser.write(b'Hello, Arduino!')
				#print("Time out...")
		except:
			if temp == "emergency":
				#pwm.ChangeDutyCycle(7) #assumes as open
				time.sleep(1)
				if not eye_detect.isRunning():
						eye_detect.run()
				state = eye_detect.getState()
				if state == 0 or state == -1:
					#pwm.ChangeDutyCycle(2.5)
					time.sleep(1)
	else:
		print("No character received!")
					
print("Servo reset")
#never lumabas ng loop
