import adafruit_sht31d
import board
import ms5803py
import time
import smbus
import os
import traceback
import sys
from datetime import datetime

day_reading = 17280
hour_reading = 720
	
# Min - Max
tempC_min = float('inf')
tempC_max = float('-inf')
press_min = float('inf')
press_max = float('-inf')
humi_min = float('inf')
humi_max = float('-inf')

tempC_min_hour = float('inf')
tempC_max_hour = float('-inf')
press_min_hour = float('inf')
press_max_hour = float('-inf')
humi_min_hour = float('inf')
humi_max_hour = float('-inf')

# Acumuladores
tempSumC_day = 0;
humiditySum_day = 0;
pressSum_day = 0;

tempSumC_hour = 0;
humiditySum_hour = 0
pressSum_hour = 0

totalTempSum = 0
totalPressSum = 0
totalHumSum = 0

totalReadingCount = 0	
readingCount_hour = 0
readingCount_day = 0

#medias
average_press = 0
average_temp = 0
average_humi = 0
average_press_hour = 0
average_temp_hour = 0
average_humi_hour = 0
average_press_day = 0
average_temp_day = 0
average_humi_day = 0
aux = 2

secSensors = "/home/tecnico/agsolve/sensores/secSensors.txt"
secSht = "/home/tecnico/agsolve/sensores/secSht.txt"
secMS = "/home/tecnico/agsolve/sensores/secMS.txt"
hourSensors = "/home/tecnico/agsolve/sensores/hourSensors.txt"
hourSht = "/home/tecnico/agsolve/sensores/hourSht.txt"
hourMS = "/home/tecnico/agsolve/sensores/hour_Backup.txt"
daySensors = "/home/tecnico/agsolve/sensores/daySensors.txt"
daySht = "/home/tecnico/agsolve/sensores/daySht.txt"
dayMS = "/home/tecnico/agsolve/sensores/dayMS.txt"

writesht = "Data          Hora     Temp_atual   Temp_med   Temp_min   Temp_max   Umi_atual   Umi_med   Umi_min   Umi_max\n"
writesensors = "Data          Hora     Temp_atual   Temp_med   Temp_min   Temp_max   Press_atual   Press_med   Press_min   Press_max   Umi_atual   Umi_med   Umi_min   Umi_max\n"
writeMS = "Data          Hora     Temp_atual   Temp_med   Temp_min   Temp_max   Press_atual   Press_med   Press_min   Press_max\n"

# Escreve o cabeçalho apenas se o arquivo estiver vazio
if not os.path.isfile(secSensors) or os.path.getsize(secSensors) == 0:
    with open(secSensors, "a") as file:
        file.write(writesensors)

if not os.path.isfile(hourSensors) or os.path.getsize(hourSensors) == 0:
    with open(hourSensors, "a") as file:
        file.write(writesensors)

if not os.path.isfile(daySensors) or os.path.getsize(daySensors) == 0:
    with open(daySensors, "a") as file:
        file.write(writesensors)

if not os.path.isfile(secSht) or os.path.getsize(secSht) == 0:
    with open(secSht, "a") as file:
        file.write(writesht)

if not os.path.isfile(hourSht) or os.path.getsize(hourSht) == 0:
    with open(hourSht, "a") as file:
        file.write(writesht)

if not os.path.isfile(daySht) or os.path.getsize(daySht) == 0:
    with open(daySht, "a") as file:
        file.write(writesht)

if not os.path.isfile(secMS) or os.path.getsize(secMS) == 0:
    with open(secMS, "a") as file:
        file.write(writeMS)
        
if not os.path.isfile(hourMS) or os.path.getsize(hourMS) == 0:
    with open(hourMS, "a") as file:
        file.write(writeMS)
        
if not os.path.isfile(dayMS) or os.path.getsize(dayMS) == 0:
    with open(dayMS, "a") as file:
        file.write(writeMS)
        
        
i2c = board.I2C()

if (aux == 2):
    try:
        sensor = adafruit_sht31d.SHT31D(i2c)
        s = ms5803py.MS5803()
        press, temp = s.read(pressure_osr=512)
        humidity = sensor.relative_humidity
        print(writesensors)
    except Exception as e:
        try:
            s = ms5803py.MS5803()
            press, temp = s.read(pressure_osr=512)
            print(writeMS)
        except Exception as e:
            try:
                sensor = adafruit_sht31d.SHT31D(i2c)
                humidity = sensor.relative_humidity
                temp = sensor.temperature
            except Exception as e:
                # Aqui você pode capturar o erro se necessário
                print(f"Erro ao inicializar os sensores: {e}")
		

while True:
    bus = smbus.SMBus(1)
    time.sleep(1)

    i2c = board.I2C()
    now = datetime.now()
    date = now.date()
    current_time = f"{now.hour:02}:{now.minute:02}:{now.second:02}"
		
    try:
        sensor = adafruit_sht31d.SHT31D(i2c)
        s = ms5803py.MS5803()
        press, temp = s.read(pressure_osr=512)
        humidity = sensor.relative_humidity
		
		#min/max temp/press
        if(temp > tempC_max):
            tempC_max = temp
        if (temp < tempC_min):
            tempC_min = temp
        if(temp > tempC_max_hour):
            tempC_max_hour = temp
        if (temp < tempC_min_hour):
            tempC_min_hour = temp
				
        if(press > press_max):
            press_max = press
        if(press < press_min):
            press_min = press
        if(press > press_max_hour):
            press_max_hour = press
        if(press < press_min_hour):
            press_min_hour = press
			
        if(humidity > humi_max):
            humi_max = humidity
        if(humidity < humi_min):
            humi_min = humidity
        if(humidity > humi_max_hour):
            humi_max_hour = humidity
        if(humidity < humi_min_hour):
            humi_min_hour = humidity
				
				
		#acum average
        totalTempSum  += temp;
        tempSumC_hour += temp
        tempSumC_day += temp
			
        totalPressSum += press
        pressSum_hour += press
        pressSum_day += press
			
        totalHumSum   += humidity
        humiditySum_day += humidity
        humiditySum_hour += humidity
			
        totalReadingCount = totalReadingCount+1
			
        if(totalReadingCount > 0): 
            average_temp = totalTempSum / totalReadingCount  
            average_press = totalPressSum / totalReadingCount
            average_humi =totalHumSum / totalReadingCount
			
        print(f"{date}   {current_time}   {temp:.2f}°C     {average_temp:.2f}°C     {tempC_min:.2f}°C   {tempC_max:.2f}°C   {press:.2f}mbar  {average_press:.2f}mbar  {press_min:.2f}mbar  {press_max:.2f}mbar   {humidity:.2f}RH   {average_humi:.2f}RH   {humi_min:.2f}RH   {humi_max:.2f}RH\n")
			
        with open(secSensors, "a") as file_append:
            file_append.write(f"{date}   {current_time}   {temp:.2f}°C     {average_temp:.2f}°C     {tempC_min:.2f}°C   {tempC_max:.2f}°C   {press:.2f}mbar  {average_press:.2f}mbar  {press_min:.2f}mbar  {press_max:.2f}mbar   {humidity:.2f}RH   {average_humi:.2f}RH   {humi_min:.2f}RH   {humi_max:.2f}RH\n")
			
			
        if(readingCount_hour < hour_reading):
            readingCount_hour = readingCount_hour+1
        if (readingCount_day < day_reading):
            readingCount_day = readingCount_day+1
				
        if(readingCount_hour == hour_reading):
            average_temp_hour = tempSumC_hour / readingCount_hour
            average_humi_hour = humiditySum_hour / readingCount_hour
            average_press_hour = pressSum_hour / readingCount_hour
            with open(hourSensors, "a") as file_append:
                file_append.write(f"{date}   {current_time}   {temp:.2f}°C     {average_temp_hour:.2f}°C     {tempC_min:.2f}°C   {tempC_max:.2f}°C   {press:.2f}mbar  {average_press_hour:.2f}mbar  {press_min:.2f}mbar  {press_max:.2f}mbar   {humidity:.2f}RH   {average_humi_hour:.2f}RH   {humi_min:.2f}RH   {humi_max:.2f}RH\n")
				
            readingCount_hour = 0;
            humiditySum_hour = 0;
            tempSumC_hour = 0;
            pressSum_hour = 0;
				
            tempC_min_hour = float('inf')
            tempC_max_hour = float('-inf')
            press_min_hour = float('inf')
            press_max_hour = float('-inf')
            humi_min_hour = float('inf')
            humi_max_hour = float('-inf')
			
        if(readingCount_day == day_reading):
            average_temp_day = tempSumC_day/day_reading
            average_humi_day = humiditySum_day/day_reading
            average_press_day = pressSum_day/day_reading
            with open(daySensors, "a") as file_append:
                file_append.write(f"{date}   {current_time}   {temp:.2f}°C     {average_temp_day:.2f}°C     {tempC_min:.2f}°C   {tempC_max:.2f}°C   {press:.2f}mbar  {average_press_day:.2f}mbar  {press_min:.2f}mbar  {press_max:.2f}mbar   {humidity:.2f}RH   {average_humi_day:.2f}RH   {humi_min:.2f}RH   {humi_max:.2f}RH\n")	
		
#############Tenta ler barômetro
    except Exception as e:
        try:
            s = ms5803py.MS5803()
            press, temp = s.read(pressure_osr=512)
			
			#min/max temp/press
            if(temp > tempC_max):
                tempC_max = temp
            if (temp < tempC_min):
                tempC_min = temp
            if(temp > tempC_max_hour):
                tempC_max_hour = temp
            if (temp < tempC_min_hour):
                tempC_min_hour = temp
						
            if(press > press_max):
                press_max = press
            if(press < press_min):
                press_min = press
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
				
            print(f"{date}   {current_time}   {temp:.2f}°C     {average_temp:.2f}°C     {tempC_min:.2f}°C   {tempC_max:.2f}°C    {press:.2f}mbar    {average_press:.2f}mbar    {press_min:.2f}mbar   {press_max:.2f}mbar\n")
            with open(secMS, "a") as file_append:
                file_append.write(f"{date}   {current_time}   {temp:.2f}°C     {average_temp:.2f}°C     {tempC_min:.2f}°C   {tempC_max:.2f}°C    {press:.2f}mbar  {average_press:.2f}mbar  {press_min:.2f}mbar  {press_max:.2f}mbar\n")
				
            if(readingCount_hour < hour_reading):
                readingCount_hour = readingCount_hour+1
            if (readingCount_day < day_reading):
                readingCount_day = readingCount_day+1
					
            if(readingCount_hour == hour_reading):
                average_temp_hour = tempSumC_hour / readingCount_hour
                average_press_hour = pressSum_hour / readingCount_hour
                with open(hourMS, "a") as file_append:
                    file_append.write(f"{date}   {current_time}   {temp:.2f}°C     {average_temp_hour:.2f}°C     {tempC_min:.2f}°C   {tempC_max:.2f}°C    {press:.2f}mbar  {average_press_hour:.2f}mbar  {press_min:.2f}mbar  {press_max:.2f}mbar\n")
					
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
                with open(dayMS, "a") as file_append:
                    file_append.write(f"{date}   {current_time}   {temp:.2f}°C     {average_temp_day:.2f}°C     {tempC_min:.2f}°C   {tempC_max:.2f}°C    {press:.2f}mbar  {average_press_day:.2f}mbar  {press_min:.2f}mbar  {press_max:.2f}mbar\n")
					
################Tenta ler SHT31
        except Exception as e:
            try:
		
                sensor = adafruit_sht31d.SHT31D(i2c)
                humidity = sensor.relative_humidity
                temp = sensor.temperature
					
                if(temp > tempC_max):
                    tempC_max = temp
                if (temp < tempC_min):
                    tempC_min = temp
				
                if(humidity > humi_max):
                    humi_max = humidity
                if(humidity < humi_min):
                    humi_min = humidity
					
                if(temp > tempC_max_hour):
                    tempC_max_hour = temp
                if (temp < tempC_min_hour):
                    tempC_min_hour = temp
						
                if(humidity > humi_max_hour):
                    humi_max_hour = humidity
                if(humidity < humi_min_hour):
                    humi_min_hour = humidity
						
				#acum average
                totalTempSum  += temp;
                tempSumC_hour += temp
                tempSumC_day += temp
					
                totalHumSum   += humidity
                humiditySum_day += humidity
                humiditySum_hour += humidity
					
                totalReadingCount = totalReadingCount+1
					
                if(totalReadingCount > 0): 
                    average_temp = totalTempSum / totalReadingCount  
                    average_humi =totalHumSum / totalReadingCount
					
                print(f"{date}   {current_time}   {temp:.2f}°C     {average_temp:.2f}°C     {tempC_min:.2f}°C   {tempC_max:.2f}°C    {humidity:.2f}RH    {average_humi:.2f}RH    {humi_min:.2f}RH   {humi_max:.2f}RH\n")
					
                with open(secMS, "a") as file_append:
                    file_append.write(f"{date}   {current_time}   {temp:.2f}°C     {average_temp:.2f}°C     {tempC_min:.2f}°C   {tempC_max:.2f}°C    {humidity:.2f}RH    {average_humi:.2f}RH    {humi_min:.2f}RH   {humi_max:.2f}RH\n")
					
                if(readingCount_hour < hour_reading):
                    readingCount_hour = readingCount_hour+1
                if (readingCount_day < day_reading):
                    readingCount_day = readingCount_day+1	
						
                if(readingCount_hour == hour_reading):
                    average_temp_hour = tempSumC_hour / readingCount_hour
                    average_humi_hour = humiditySum_hour / readingCount_hour
                    with open(hourSHT, "a") as file_append:
                        file_append.write(f"{date}   {current_time}   {temp:.2f}°C     {average_temp_hour:.2f}°C     {tempC_min:.2f}°C   {tempC_max:.2f}°C    {humidity:.2f}RH    {average_humi_hour:.2f}RH    {humi_min:.2f}RH   {humi_max:.2f}RH\n")
						
                    readingCount_hour = 0;
                    humiditySum_hour = 0;
                    tempSumC_hour = 0;
                    pressSum_hour = 0;
						
                    tempC_min_hour = float('inf')
                    tempC_max_hour = float('-inf')
                    press_min_hour = float('inf')
                    press_max_hour = float('-inf')
                    humi_min_hour = float('inf')
                    humi_max_hour = float('-inf')
					
                if(readingCount_day == day_reading):
                    average_temp_day = tempSumC_day/day_reading
                    average_humi_day = humiditySum_day/day_reading
                    with open(daySHT, "a") as file_append:
                        file_append.write(f"{date}   {current_time}   {temp:.2f}°C     {average_temp_day:.2f}°C     {tempC_min:.2f}°C   {tempC_max:.2f}°C    {humidity:.2f}RH    {average_humi_day:.2f}RH    {humi_min:.2f}RH   {humi_max:.2f}RH\n")
			
            except Exception as e:
                now = datetime.now()
                date = now.date()
                current_time = f"{now.hour:02}:{now.minute:02}:{now.second:02}"
		
                error_message = f"{date} {current_time} Erro: {e}. Tentando novamente em 5 segundos...\n"
                print(error_message)
				
        time.sleep(5)