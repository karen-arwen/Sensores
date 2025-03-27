# SHT31 X DS18B20
I2C & 1WIRE
<table>
<tr>
<td>
<img src="https://cdn.awsli.com.br/600x700/468/468162/produto/19414360586929efad.jpg" width=200px height=200px display=inline-block>
</td>
<td>
<img src="https://www.plexishop.it/media/catalog/product/cache/3/image/650x/040ec09b1e35df139433887a97daa66f/m/o/modulo_gy-sht30-d_sensore_digitale_di_temperatura_e_umidit_2.jpg" width=200px height=200px display= inline-block>
</td>
 </tr>
</table>

<h1></h1>

<b><h4>SHT31xDS18B20</h4></b>
O diretório <b>Sht31xDs18b20</b> é onde está guardado o códigos referente aos sensores SHT31 e DS18B20, que recebe os dados de Temperatura — e Umidade (SHT31).
O código tem a implementação com o Banco de Dados e o Google Sheets, transmitindo dados de maneira automática (Se houver internet).

<h1></h1>

<br>
<b><i>Não esqueça de verificar se aS interfaces I2C E 1W estão habilitadas!!</i></b>
<br>
<p><i>Para habilitar é necessário executar <code>raspi-config</code>, vá até a aba <code>interface</code>, habilite o I2C e 1w, e logo após dê um <code>reboot</code> para que as mudanças sejam implementadas. </i></p>
<br>

<h1>Google Sheets</h1>
<p>Foram criadas planilhas que recebem os dados de maneira automática ao se rodar o programa, aqui estão as planilhas com os resultados e dashboard dos testes dos sensores, feitos no calor e frio: </p>

<h3>Calor</h3>

<b><a href="https://docs.google.com/spreadsheets/d/1fL7DO_MSp1J5JL7bz_20hxTic1TAMUOj3dbih8Of5hk/edit?usp=sharing">Calor Seg</a></b> <br>
<b><a href="https://docs.google.com/spreadsheets/d/1JevTcL4XpLGiWSPRLXUIWwXjGKEKdRm-Q7S8gW_3hxs/edit?usp=sharing">Calor Hora</a></b> <br>
<b><a href="https://docs.google.com/spreadsheets/d/16OXg0T6HdTGaumcgu4zzyrobzL-7_YNoPFPb_YMeOko/edit?usp=sharing">Calor Dashboard</a></b> <br> <br>

<h3>Frio</h3>
<b><a href="https://docs.google.com/spreadsheets/d/1tKKv-M5eFFnKrx8E9ZY9380NUurK_hSlsEs4N98pDnY/edit?usp=sharing">Frio Seg</a></b> <br>
<b><a href="https://docs.google.com/spreadsheets/d/1MsTD1-EiRxMioHX0k5BLjNBS7pZgZdvaiKVDcoSrpiw/edit?usp=sharing">Frio Hora</a></b> <br>
<b><a href="https://docs.google.com/spreadsheets/d/1mh9MuUTP4ev7zRZsireCwAEC1ZbluOG25wb8M8JyEcM/edit?usp=sharing">Frio Dashboard</a></b> <br>


<h1></h1>

<h3> <p>Links Importantes: </p> </h3>
<p> https://randomnerdtutorials.com/raspberry-pi-ds18b20-python/
<p> https://medium.com/@jb.ranchana/write-and-append-dataframes-to-google-sheets-in-python-f62479460cf0


<h1></h1>
<h5>Importante!!</h5> 

Todos os códigos aqui encontrados possuem a função de escrever esses dados recebidos em arquivos backup.txt, sendo eles:
- *SEC_BACKUP.TXT* -> Escreve de 5 em 5 segundos a leitura realizada pelos sensores (Bom para monitoramento).
- *HOUR_BACKUP.TXT* -> Escreve de 1 em 1 hora a leitura realizada pelos sensores.
- *DAY_BACKUP.TXT* -> Escreve de 1 em 1 dia (24 horas) a leitura realizada pelos sensores
 
*Necessário mudar caminho dos arquivos .TXT para que possam ser gravados corretamente*
<h1></h1>


