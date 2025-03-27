import adafruit_sht31d, board, ms5803py,time, smbus,os, traceback,sys, time
from datetime import datetime

day_reading = 17280
hour_reading = 720
	
# Min - Max
tempC_min = float('inf')
tempC_max = float('-inf')
humi_min = float('inf')
humi_max = float('-inf')

tempC_min_hour = float('inf')
tempC_max_hour = float('-inf')
humi_min_hour = float('inf')
humi_max_hour = float('-inf')

# Acumuladores
tempSumC_day = 0;
humiditySum_day = 0;

tempSumC_hour = 0;
humiditySum_hour = 0

totalTempSum = 0
totalHumSum = 0

totalReadingCount = 0	
readingCount_hour = 0
readingCount_day = 0

#medias
average_temp = 0
average_humi = 0
average_temp_hour = 0
average_humi_hour = 0
average_temp_day = 0
average_humi_day = 0

aux = 2

sec_backup = "/home/tecnico/agsolve/temp_umi_sensor/sec_backup_py.txt"
hour_backup = "/home/tecnico/agsolve/temp_umi_sensor/hour_backup_py.txt"
day_backup = "/home/tecnico/agsolve/temp_umi_sensor/day_backup_py.txt"

writesht = "Data          Hora     Temp_atual   Temp_med   Temp_min   Temp_max   Umi_atual   Umi_med   Umi_min   Umi_max\n"

# Escreve o cabeçalho apenas se o arquivo estiver vazio
if not os.path.isfile(sec_backup) or os.path.getsize(sec_backup) == 0:
    with open(sec_backup, "a") as file:
        file.write(writesht)

if not os.path.isfile(hour_backup) or os.path.getsize(hour_backup) == 0:
    with open(hour_backup, "a") as file:
        file.write(writesht)

if not os.path.isfile(day_backup) or os.path.getsize(day_backup) == 0:
    with open(day_backup, "a") as file:
        file.write(writesht)
        
print(writesht)

while True:
    
    bus = smbus.SMBus(1)
    time.sleep(1)

    i2c = board.I2C()
    now = datetime.now()
    date = now.date()
    current_time = f"{now.hour:02}:{now.minute:02}:{now.second:02}"
		
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
					
        with open(sec_backup, "a") as file_append:
            file_append.write(f"{date}   {current_time}   {temp:.2f}°C     {average_temp:.2f}°C     {tempC_min:.2f}°C   {tempC_max:.2f}°C    {humidity:.2f}RH    {average_humi:.2f}RH    {humi_min:.2f}RH   {humi_max:.2f}RH\n")
					
					
        if(readingCount_hour < hour_reading):
            readingCount_hour = readingCount_hour+1
        if (readingCount_day < day_reading):
            readingCount_day = readingCount_day+1
					
						
        if(readingCount_hour == hour_reading):
            average_temp_hour = tempSumC_hour / readingCount_hour
            average_humi_hour = humiditySum_hour / readingCount_hour
            
            with open(hour_backup, "a") as file_append:
                file_append.write(f"{date}   {current_time}   {temp:.2f}°C     {average_temp_hour:.2f}°C     {tempC_min:.2f}°C   {tempC_max:.2f}°C    {humidity:.2f}RH    {average_humi_hour:.2f}RH    {humi_min:.2f}RH   {humi_max:.2f}RH\n")
                
            readingCount_hour = 0;
            humiditySum_hour = 0;
            tempSumC_hour = 0;
						
            tempC_min_hour = float('inf')
            tempC_max_hour = float('-inf')
            humi_min_hour = float('inf')
            humi_max_hour = float('-inf')
					
        if(readingCount_day == day_reading):
            average_temp_day = tempSumC_day/day_reading
            average_humi_day = humiditySum_day/day_reading
            
            with open(day_backup, "a") as file_append:
                file_append.write(f"{date}   {current_time}   {temp:.2f}°C     {average_temp_day:.2f}°C     {tempC_min:.2f}°C   {tempC_max:.2f}°C    {humidity:.2f}RH    {average_humi_day:.2f}RH    {humi_min:.2f}RH   {humi_max:.2f}RH\n")
			
    except Exception as e:
        now = datetime.now()
        date = now.date()
        current_time = f"{now.hour:02}:{now.minute:02}:{now.second:02}"
		
        error_message = f"{date} {current_time} Erro: {e}. Tentando novamente em 5 segundos...\n"
        print(error_message)
        with open(sec_backup, "a") as file_append:
            file_append.write(error_message)
		
        		
    time.sleep(5) 
        