import adafruit_sht31d
import board
import traceback
from datetime import datetime
import smbus
import time
import os
import glob
import schedule
from datetime import datetime, timedelta
import sys
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import get_as_dataframe, set_with_dataframe
import pymysql


HOST = "10.0.170.19" # = "localhost"
PORT = 3306 # "Padrão"
USER_DB = "root" # usuário ("gerente")
PASS_DB = "@F=1R8*9" #senha p entrar
BASE = "agdados" # "teste" -> database

#Conecta ao banco de dados
conn = pymysql.connect(host = HOST, port = PORT, user = USER_DB ,passwd = PASS_DB, db = BASE)
# conn = mariadb.connect(host = HOST, port = 3306, user = USER_DB ,password = PASS_DB, database = BASE)

conn.auto_reconnect = True
cursor = conn.cursor()

#escopo utilizado
scope = ['https://www.googleapis.com/auth/spreadsheets']

#dados de autenticação
credentials = ServiceAccountCredentials.from_json_keyfile_name('/home/tecnico/agsolve/temperatureSensors/temp_frio.json',scope)
gc = gspread.authorize(credentials)
worksheet   = gc.open_by_key('1tKKv-M5eFFnKrx8E9ZY9380NUurK_hSlsEs4N98pDnY').get_worksheet(0) #ambos - sec 
worksheet1  = gc.open_by_key('1tKKv-M5eFFnKrx8E9ZY9380NUurK_hSlsEs4N98pDnY').get_worksheet(1) #SHT31 - sec
worksheet2  = gc.open_by_key('1tKKv-M5eFFnKrx8E9ZY9380NUurK_hSlsEs4N98pDnY').get_worksheet(2) #DS18B20 - sec
worksheetH  = gc.open_by_key('1MsTD1-EiRxMioHX0k5BLjNBS7pZgZdvaiKVDcoSrpiw').get_worksheet(0) #ambos - h 
worksheetH1 = gc.open_by_key('1MsTD1-EiRxMioHX0k5BLjNBS7pZgZdvaiKVDcoSrpiw').get_worksheet(1) #SHT31 - h
worksheetH2 = gc.open_by_key('1MsTD1-EiRxMioHX0k5BLjNBS7pZgZdvaiKVDcoSrpiw').get_worksheet(2) #DS18B20 - h


hour = '07:00:00'   #Definição de horário para o backup diário
hours = [ '00:00:00','01:00:00','02:00:00','03:00:00','04:00:00', #backup de 1 em 1hr por 24h
          '05:00:00','06:00:00','07:00:00','08:00:00','09:00:00',
          '10:00:00','11:00:00','12:00:00','13:00:00','14:00:00',
          '15:00:00','16:00:00','17:00:00','18:00:00','19:00:00',
          '20:00:00','21:00:00','22:00:00','23:00:00', 
          '00:59:59','01:59:59','02:59:59','03:59:59','04:59:59', #backup de 1 em 1hr por 24h
          '05:59:59','06:59:59','07:59:59','08:59:59','09:59:59',
          '10:59:59','11:59:59','12:59:59','13:59:59','14:59:59',
          '15:59:59','16:59:59','17:59:59','18:59:59','19:59:59',
          '20:59:59','21:59:59','22:59:59','23:59:59']


tempC_min_sht = float('inf')              
tempC_min_ds = float('inf')
tempC_max_sht = float('-inf')
tempC_max_ds = float('-inf')
humidity_min_sht = float('inf')
humidity_max_sht = float('-inf')
tempC_min_hour_sht = float('inf')
tempC_min_hour_ds = float('inf')
tempC_max_hour_sht = float('-inf')
tempC_max_hour_ds = float('-inf')
humidity_min_hour_sht = float('inf')
humidity_max_hour_sht = float('-inf')

# Acumuladores
seconds = 1
sec = 1
tempSumC_day_sht = 0
tempSumC_day_ds = 0
humiditySum_day_sht = 0

tempSumC_hour_sht = 0
tempSumC_hour_ds = 0
humiditySum_hour_sht = 0

totalTempSum_sht  = 0
totalTempSum_ds  = 0
totalhumiditySum_sht = 0
totalReadingCount = 0	
readingCount_hour = 0
readingCount_day  = 0

average_humidity_sht = 0
average_temp_sht  = 0
average_temp_ds  = 0
average_humidity_hour_sht = 0
average_temp_hour_sht  = 0
average_temp_hour_ds  = 0
average_humidity_day_sht  = 0
average_temp_day_sht   = 0
average_temp_day_ds   = 0

secBackup_sht  = "/home/tecnico/agsolve/temperatureSensors/sec_Backup_sht.txt"
hourBackup_sht = "/home/tecnico/agsolve/temperatureSensors/hour_Backup_sht.txt"
dayBackup_sht  = "/home/tecnico/agsolve/temperatureSensors/day_Backup_sht.txt"

secBackup_ds  = "/home/tecnico/agsolve/temperatureSensors/sec_Backup_ds.txt"
hourBackup_ds = "/home/tecnico/agsolve/temperatureSensors/hour_Backup_ds.txt"
dayBackup_ds  = "/home/tecnico/agsolve/temperatureSensors/day_Backup_ds.txt"

hourBackup = "/home/tecnico/agsolve/temperatureSensors/hour_Backup.txt"
dayBackup  = "/home/tecnico/agsolve/temperatureSensors/day_Backup.txt"

backupSec_existe_sht = os.path.isfile(secBackup_sht) and os.path.getsize(secBackup_sht) > 0
backupHour_existe_sht = os.path.isfile(hourBackup_sht) and os.path.getsize(hourBackup_sht) > 0
backupDay_existe_sht = os.path.isfile(dayBackup_sht) and os.path.getsize(dayBackup_sht) > 0

backupSec_existe_ds = os.path.isfile(secBackup_ds) and os.path.getsize(secBackup_ds) > 0
backupHour_existe_ds = os.path.isfile(hourBackup_ds) and os.path.getsize(hourBackup_ds) > 0
backupDay_existe_ds = os.path.isfile(dayBackup_ds) and os.path.getsize(dayBackup_ds) > 0

backupHour_existe = os.path.isfile(hourBackup) and os.path.getsize(hourBackup) > 0
backupDay_existe = os.path.isfile(dayBackup) and os.path.getsize(dayBackup) > 0

write_header = "Data          Hora     Disp   Temp_atual       Temp_med         Temp_min        Temp_max        Humi_atual     Humi_med      Humi_min       Humi_max\n"
write_header2 = "Data          Hora     Disp   Temp_atual       Temp_med         Temp_min        Temp_max\n"

with open(secBackup_sht, "a") as file:
    # Escreve o cabeçalho apenas se o arquivo estiver vazio
    if not backupSec_existe_sht:
        file.write(write_header)
        
with open(secBackup_ds, "a") as file:
    # Escreve o cabeçalho apenas se o arquivo estiver vazio
    if not backupSec_existe_ds:
        file.write(write_header2)
        
with open(hourBackup, "a") as file:
    if not backupHour_existe:
        file.write(write_header)
        
with open(hourBackup_sht, "a") as file:
    if not backupHour_existe_sht:
        file.write(write_header)
        
with open(hourBackup_ds, "a") as file:
    if not backupHour_existe_sht:
        file.write(write_header2)
        
with open(dayBackup, "a") as file:
    if not backupDay_existe:
        file.write(write_header)
        
with open(dayBackup_sht, "a") as file:
    if not backupDay_existe_sht:
        file.write(write_header)

with open(dayBackup_ds, "a") as file:
    if not backupDay_existe_ds:
        file.write(write_header2)
        
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.1)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

#Função para inserir os dados no banco de dados
def insert(conn, cursor, field_id, value, timestamp):
    #query = ("INSERT IGNORE INTO tbldata(dat_StationFieldID, dat_Value, dat_Datetime, dat_ValueOriginal) VALUES ('" + \
    query = ("INSERT IGNORE INTO tbldatart(rt_StationFieldID, rt_Value, rt_Datetime, rt_ValueOriginal) VALUES ('" + \
    str(field_id) + "'," + str(value) + ",'" + str(timestamp) + "'," + str(value) + ")")
    # print(query)
    cursor.execute(query)
    conn.commit()
		
print (write_header)

while True:

    bus = smbus.SMBus(1)
    time.sleep(1)
    i2c = board.I2C()
    
    try:
        
        now = datetime.now()
        data = now.strftime('%d/%m/%Y')
        date = data
        current_time = now.strftime('%H:%M:%S')
        hora = current_time
        day_time = now.strftime("%Y/%m/%d %H:%M:%S")

        sensor = adafruit_sht31d.SHT31D(i2c)
        humidity_sht = sensor.relative_humidity
        cTemp_sht = sensor.temperature
        cTemp_ds = (read_temp())
        
        seconds += 1    
        sec +=1 
        
            	
        if(totalReadingCount > 0): 
                average_temp_sht = totalTempSum_sht / totalReadingCount  
                average_temp_ds = totalTempSum_ds / totalReadingCount  
                average_humidity_sht = totalhumiditySum_sht / totalReadingCount
    
        if (seconds == 2):	
            if(cTemp_sht > tempC_max_sht):
                tempC_max_sht = cTemp_sht
            if (cTemp_sht < tempC_min_sht):
                tempC_min_sht = cTemp_sht
            if(cTemp_sht > tempC_max_hour_sht):
                tempC_max_hour_sht = cTemp_sht
            if (cTemp_sht < tempC_min_hour_sht):
                tempC_min_hour_sht = cTemp_sht
                        
            if(humidity_sht > humidity_max_sht):
                humidity_max_sht = humidity_sht
            if(humidity_sht < humidity_min_sht):
                humidity_min_sht = humidity_sht
            if(humidity_sht > humidity_max_hour_sht):
                humidity_max_hour_sht = humidity_sht
            if(humidity_sht < humidity_min_hour_sht):
                humidity_min_hour_sht = humidity_sht
                
            if(cTemp_ds > tempC_max_ds):
                tempC_max_ds = cTemp_ds
            if (cTemp_ds < tempC_min_ds):
                tempC_min_ds = cTemp_ds
            if(cTemp_ds > tempC_max_hour_ds):
                tempC_max_hour_ds = cTemp_ds
            if (cTemp_ds < tempC_min_hour_ds):
                tempC_min_hour_ds = cTemp_ds
                        
               
            totalReadingCount = totalReadingCount+1   
            #acum average
            totalTempSum_sht  += cTemp_sht
            totalTempSum_ds  += cTemp_ds
            tempSumC_hour_sht += cTemp_sht
            tempSumC_hour_ds += cTemp_ds
            tempSumC_day_sht  += cTemp_sht
            tempSumC_day_ds  += cTemp_ds
                    
            totalhumiditySum_sht += humidity_sht
            humiditySum_hour_sht += humidity_sht
            humiditySum_day_sht  += humidity_sht
            readingCount_hour +=1
            readingCount_day +=1
            
            print(f"{date}   {current_time}   1     {cTemp_sht:.2f}\t\t{average_temp_sht:.2f}\t\t{tempC_min_sht:.2f}\t\t{tempC_max_sht:.2f}\t\t{humidity_sht:.2f}\t\t{average_humidity_sht:.2f}\t\t{humidity_min_sht:.2f}\t\t{humidity_max_sht:.2f}\n")   
            print(f"                        2     {cTemp_ds:.2f}\t\t{average_temp_ds:.2f}\t\t{tempC_min_ds:.2f}\t\t{tempC_max_ds:.2f}\t\t\n")
        
            with open(secBackup_sht, "a") as file_append:
                file_append.write(f"{date}   {current_time}   1     {cTemp_sht:.2f}\t\t{average_temp_sht:.2f}\t\t{tempC_min_sht:.2f}\t\t{tempC_max_sht:.2f}\t\t{humidity_sht:.2f}\t\t{average_humidity_sht:.2f}\t\t{humidity_min_sht:.2f}\t\t{humidity_max_sht:.2f}\n")   
            with open(secBackup_ds, "a") as file_append:
                file_append.write(f"{date}   {current_time}   2     {cTemp_ds:.2f}\t\t{average_temp_ds:.2f}\t\t{tempC_min_ds:.2f}\t\t{tempC_max_ds:.2f}\t\t\n")   
            try:
                barr_1 = [date, current_time, "SHT31", cTemp_sht, humidity_sht ]
                worksheet.append_row(barr_1)
                barr_2 = [date, current_time, "DS18B20", cTemp_ds]
                worksheet.append_row(barr_2)
                
                barr_1 = [date, current_time, cTemp_sht, humidity_sht ]
                worksheet1.append_row(barr_1)
                barr_2 = [date, current_time, cTemp_ds]
                worksheet2.append_row(barr_2)
            except Exception as e:
                print(f"{date} {current_time} Erro: {e}. Tentando novamente...\n Erro ao colocar na planilha Sec.")
                
                
            try:
                if (sec == 12 ):    
                    cursor.execute("SELECT MAX(rt_Value) FROM tbldatart WHERE rt_StationFieldID = 4 ")
                    temp_max_ds_bcd = cursor. fetchone()[0] 
                    cursor.execute("SELECT MIN(rt_Value) FROM tbldatart WHERE rt_StationFieldID = 4")
                    temp_min_ds_bcd = cursor. fetchone()[0]  
                        
                    #Insere os dados no BCD. Ex das informações
                    #[ Posição | Field | CAMPO   ]
                    #|    1    |   4   |Temp Int |
                    #|    2    |   7   |Temp Min |
                    #|    3    |   8   |Temp Max |
                    #[    4    |   6   |Pressão  ]
                    
                    #insert(conn, cur, field_id, value, timestamp)
                    insert(conn, cursor, 4, cTemp_ds , day_time)
                    insert(conn, cursor, 9, cTemp_sht, day_time)

                    #insert(conn, cursor, 7, temp_min_ds_bcd, day_time)
                    #insert(conn, cursor, 8, temp_max_ds_bcd, day_time)
                    sec = 0
                                
            except Exception as e:
                print(f"Error to insert data in database: {e}")
                conn.rollback()

            
            seconds = 0	
            
        
        
        if hora in hours:
            average_temp_hour_sht = tempSumC_hour_sht  / readingCount_hour
            average_temp_hour_ds = tempSumC_hour_ds  / readingCount_hour
            average_humidity_hour_sht = humiditySum_hour_sht / readingCount_hour
                
            with open(hourBackup_sht, "a") as file_append:
                file_append.write(f"{date}   {current_time}   1     {cTemp_sht:.2f}\t\t{average_temp_hour_sht:.2f}\t\t{tempC_min_sht:.2f}\t\t{tempC_max_sht:.2f}\t\t{humidity_sht:.2f}\t\t{average_humidity_hour_sht:.2f}\t\t{humidity_min_sht:.2f}\t\t{humidity_max_sht:.2f}\n")
            with open(hourBackup_ds, "a") as file_append:
                file_append.write(f"{date}   {current_time}   2     {cTemp_ds:.2f}\t\t{average_temp_hour_ds:.2f}\t\t{tempC_min_ds:.2f}\t\t{tempC_max_ds:.2f}\t\n")
            with open(hourBackup, "a") as file_append:
                file_append.write(f"{date}   {current_time}   1     {cTemp_sht:.2f}\t\t{average_temp_hour_sht:.2f}\t\t{tempC_min_sht:.2f}\t\t{tempC_max_sht:.2f}\t\t{humidity_sht:.2f}\t\t{average_humidity_hour_sht:.2f}\t\t{humidity_min_sht:.2f}\t\t{humidity_max_sht:.2f}\n")   
                file_append.write(f"                        2     {cTemp_ds:.2f}\t\t{average_temp_hour_ds:.2f}\t\t{tempC_min_ds:.2f}\t\t{tempC_max_ds:.2f}\n\n")
            
            try: 
                barr_1 = [date, current_time, "SHT31", cTemp_sht, humidity_sht]
                worksheetH.append_row(barr_1)
                barr_2 = [date, current_time, "DS18B20", cTemp_ds]
                worksheetH.append_row(barr_2)
                
                barr_1 = [date, current_time,cTemp_sht,humidity_sht]
                worksheetH1.append_row(barr_1)
                barr_2 = [date, current_time, cTemp_ds]
                worksheetH2.append_row(barr_2)

            except Exception as e :
                print(f"{date} {current_time} Erro: {e}. Tentando novamente...\n. Não foi possivel gravar seus arquivos na planilha HORA {e}")


            readingCount_hour  = 0
            tempSumC_hour_sht = 0
            tempSumC_hour_ds = 0
            humiditySum_hour_sht = 0
                
            tempC_min_hour_sht = float('-inf')
            tempC_min_hour_ds = float('inf')
            tempC_max_hour_sht = float('-inf')
            tempC_max_hour_ds = float('-inf')
            humidity_min_hour_sht = float('-inf')
            humidity_max_hour_sht = float('-inf')
        
        if hora in hour:
            average_temp_day_sht = tempSumC_day_sht/readingCount_day
            average_temp_day_ds = tempSumC_day_ds/readingCount_day
            average_humidity_day_sht = humiditySum_day_sht/readingCount_day
            
            with open(dayBackup_sht, "a") as file_append:
                file_append.write(f"{date}   {current_time}   1     {cTemp_sht:.2f}\t\t{average_temp_day_sht:.2f}\t\t{tempC_min_sht:.2f}\t\t{tempC_max_sht:.2f}\t\t{humidity_sht:.2f}\t\t{average_humidity_day_sht:.2f}\t\t{humidity_min_sht:.2f}\t\t{humidity_max_sht:.2f}\n")
            with open(dayBackup_ds, "a") as file_append:
                file_append.write(f"{date}   {current_time}   2     {cTemp_ds:.2f}\t\t{average_temp_day_ds:.2f}\t\t{tempC_min_ds:.2f}\t\t{tempC_max_ds:.2f}\n")
            with open(dayBackup, "a") as file_append:
                file_append.write(f"{date}   {current_time}   1     {cTemp_sht:.2f}\t\t{average_temp_day_sht:.2f}\t\t{tempC_min_sht:.2f}\t\t{tempC_max_sht:.2f}\t\t{humidity_sht:.2f}\t\t{average_humidity_day_sht:.2f}\t\t{humidity_min_sht:.2f}\t\t{humidity_max_sht:.2f}\n")
                file_append.write(f"                        2     {cTemp_ds:.2f}\t\t{average_temp_day_ds:.2f}\t\t{tempC_min_ds:.2f}\t\t{tempC_max_ds:.2f}\n\n")

            readingCount_day  = 0
            tempSumC_day_sht = 0
            tempSumC_day_ds = 0
            humiditySum_day_sht = 0
    
    except Exception as e:
        now = datetime.now()
        date = now.date()
        current_time = f"{now.hour:02}:{now.minute:02}:{now.second:02}"
        error_message = f"{date} {current_time} Erro: {e}. Tentando novamente...\n"
        print(error_message)
        time.sleep(1)
        