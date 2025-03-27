import board
import ms5803py
import time
from datetime import datetime
import smbus
import os
import traceback

day_reading = 17280
hour_reading = 720
	
# #
tempC_min = float('inf')
tempC_max = float('-inf')
press_min = float('inf')
press_max = float('-inf')

tempC_min_hour = float('inf')
tempC_max_hour = float('-inf')
press_min_hour = float('inf')
press_max_hour = float('-inf')

# Acumuladores
tempSumC_day = 0;
pressSum_day = 0;
##                ##
tempSumC_hour = 0;
pressSum_hour = 0
#
totalTempSum = 0
totalPressSum = 0
#
totalReadingCount = 0	
readingCount_hour = 0
readingCount_day = 0
#
average_press = 0
average_temp = 0
average_press_hour = 0
average_temp_hour = 0
average_press_day = 0
average_temp_day = 0



secBackup = "/home/tecnico/agsolve/pressure_sensor/sec_Backup.txt"
hourBackup = "/home/tecnico/agsolve/pressure_sensor/hour_Backup.txt"
dayBackup = "/home/tecnico/agsolve/pressure_sensor/day_Backup.txt"

backupSec_existe = os.path.isfile(secBackup) and os.path.getsize(secBackup) > 0
backupHour_existe = os.path.isfile(hourBackup) and os.path.getsize(hourBackup) > 0
backupDay_existe = os.path.isfile(dayBackup) and os.path.getsize(dayBackup) > 0

write_header = "Data          Hora     Temp_atual   Temp_med   Temp_min   Temp_max   Press_atual   Press_med   Press_min   Press_max\n"
with open(secBackup, "a") as file:
	if not backupSec_existe:
		file.write(write_header)

with open(hourBackup, "a") as file:
	if not backupHour_existe:
		file.write(write_header)

with open(dayBackup, "a") as file:
	# Escreve o cabeçalho apenas se o arquivo estiver vazio
	if not backupDay_existe:
		file.write(write_header)
		
print(write_header)

while True:
    bus = smbus.SMBus(1)
    time.sleep(1)

    i2c = board.I2C()
	
    try:
        s = ms5803py.MS5803()
        press, temp = s.read(pressure_osr=512)
        now = datetime.now()
        date = now.date()
        current_time = f"{now.hour:02}:{now.minute:02}:{now.second:02}"
        #min/max temp/press
        if(temp > tempC_max):
            tempC_max = temp
        if (temp < tempC_min):
            tempC_min = temp
				
        if(press > press_max):
            press_max = press
        if(press < press_min):
            press_min = press
		#####
        if(temp > tempC_max_hour):
            tempC_max_hour = temp
        if (temp < tempC_min_hour):
            tempC_min_hour = temp
			
        if(press > press_max_hour):
            press_max_hour = press
        if(press < press_min_hour):
            press_min_hour = press
				
		#acum average
        totalTempSum  += temp;
        tempSumC_hour += temp
        tempSumC_day += temp
			
        totalPressSum += press
        pressSum_hour += press
        pressSum_day += press
			
        totalReadingCount = totalReadingCount+1
			
        if(totalReadingCount > 0): 
            average_temp = totalTempSum / totalReadingCount  
            average_press = totalPressSum / totalReadingCount
			
        print(f"{date}   {current_time}   {temp:.2f}°C     {average_temp:.2f}°C     {tempC_min:.2f}°C   {tempC_max:.2f}°C   {press:.2f}mbar  {average_press:.2f}mbar  {press_min:.2f}mbar  {press_max:.2f}mbar\n")
			
        with open(secBackup, "a") as file_append:
            file_append.write(f"{date}   {current_time}   {temp:.2f}°C     {average_temp:.2f}°C     {tempC_min:.2f}°C   {tempC_max:.2f}°C   {press:.2f}mbar  {average_press:.2f}mbar  {press_min:.2f}mbar  {press_max:.2f}mbar\n")
			
			
        if(readingCount_hour < hour_reading):
            readingCount_hour = readingCount_hour+1
        if (readingCount_day < day_reading):
            readingCount_day = readingCount_day+1
			
				
        if(readingCount_hour == hour_reading):
            average_temp_hour = tempSumC_hour / readingCount_hour
            average_press_hour = pressSum_hour / readingCount_hour
            with open(hourBackup, "a") as file_append:
                file_append.write(f"{date}   {current_time}   {temp:.2f}°C     {average_temp_hour:.2f}°C     {tempC_min:.2f}°C   {tempC_max:.2f}°C   {press:.2f}mbar  {average_press_hour:.2f}mbar  {press_min:.2f}mbar  {press_max:.2f}mbar\n")
    
            readingCount_hour = 0;
            tempSumC_hour = 0;
            pressSum_hour = 0;
				
            tempC_min_hour = float('inf')
            tempC_max_hour = float('-inf')
            press_min_hour = float('inf')
            press_max_hour = float('-inf')
			
        if(readingCount_day == day_reading):
            average_temp_day = tempSumC_day/day_reading
            average_press_day = pressSum_day/day_reading
            with open(dayBackup, "a") as file_append:
                file_append.write(f"{date}   {current_time}   {temp:.2f}°C     {average_temp_day:.2f}°C     {tempC_min:.2f}°C   {tempC_max:.2f}°C   {press:.2f}mbar  {average_press_day:.2f}mbar  {press_min:.2f}mbar  {press_max:.2f}mbar\n")
				
			
    except Exception as e:
        now = datetime.now()
        date = now.date()
        current_time = f"{now.hour:02}:{now.minute:02}:{now.second:02}"
    
        error_message = f"{date} {current_time} Erro: {e}. Tentando novamente em 5 segundos...\n"
        print(error_message)

        time.sleep(5)
		
	

