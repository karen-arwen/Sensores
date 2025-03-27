O código a seguir realiza a leitura dos 2 sensores. Caso 1 não esteja sendo reconhecido, ele tentará ler somente as informações do outro sensor restante, 
e escrevendo suas informações recebidas em arquivos Backup, sendo eles:
- SHT -> Sensor de temperatura e umidade
- MS -> Sensor de temperatura e pressão
- Sensores -> Ambos sensores sendo lidos juntos (SHT31+MS5803)

e tendo como parâmetro Sec ( Escreve a cada 5 segundos ) - Hour ( Escreve de 1 em 1 hora ) - Day ( Escreve de 1 em 1 dia(24h) )

Caso não consiga ler ambos, ele enviará uma mensagem mostrando qual erro ocorreu.
