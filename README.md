# sensores
<table>
 <tr>
  <td>   
    <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTEAnJ29exhYAwGashW_eJUodFbDI3EbSVMww&s" width=200px height=200px display=inline-block>
    <br>
    <p>MS5803</p>
  </td>
  <td>
   <img src="https://camo.githubusercontent.com/f8d3d0ae49ce490eb587555cd9b9a571f3e5d6930458a233c5a360238d71d0df/68747470733a2f2f7777772e6167736f6c76652e636f6d2e62722f696d6770726f6475746f732f696d6167656e732f313134315f312e6a7067"  width=200px height=200px display=inline-block>
   <br>
   <p>EME-BARO5803</p>
  </td>
 </tr>
</table>

<table>
 <tr>
  <td>
   <img src="https://www.plexishop.it/media/catalog/product/cache/3/image/650x/040ec09b1e35df139433887a97daa66f/m/o/modulo_gy-sht30-d_sensore_digitale_di_temperatura_e_umidit_2.jpg" width=200px height=200px display= inline-block>
   <br>
   <p>SHT31</p>
  </td>
  <td>
   <img src="https://www.huinfinito.com.br/1490-large_default/sensor-de-temperatura-ds18b20-prova-d-agua.jpg" width=200px height=200px display= inline-block>
   <br>
   <p>DS18B20</p>
  </td>
 </tr>
</table>

<p>É necessário os dar os seguintes comandos no terminal para que <b>todos</b> os códigos funcionem corretamente:  </p>
<code>pip install ms5803py</code>
<code>sudo pip3 install adafruit-circuitpython-sht31d</code>
<code>pip install smbus</code>
<code>sudo apt-get install i2c-tools</code>
<code>pip install matplotlib seaborn plotly pandas numpy</code>
<code>pip install gspread-dataframe</code>
<code>pip install gspread oauth2client</code>
<code>pip install numexpr</code>
<code>pip install Bottleneck</code>

<br><br>
<b><i>Não esqueça de verificar se aS interfaceS I2C E 1W estão habilitadas!!</i></b>
<br>
<p><i>Para habilitar é necessário executar <code>raspi-config</code>, vá até a aba <code>interface</code>, habilite o I2C e 1w, e logo após dê um <code>reboot</code> para que as mudanças sejam implementadas. </i></p>
<br>
<br>
<h1> Diretórios</h1>

<b><h4>SENSORS</h4></b>
O diretório **Sensors** é onde está guardado os códigos referentes ao funcionamento de todos os sensores aqui encontrados, sendo eles:  <b>SHT31, MS5803, DS18B20 e EME-BARO5803.</b> 
Recebendo os dados de Temperatura, Pressão e Umidade (Variando o recebimento de dados com a funcionalidade de cada sensor). Dentro desse diretório, encontramos os códigos na linguagem Python e C.

<h1></h1>

<b><h4>SHT31xDS18B20</h4></b>
O diretório **Sht31xDs18b20** é onde está guardado o códigos referente aos sensores SHT31 e DS18B20, que recebe os dados de Temperatura — e Umidade (SHT31).
O código tem a implementação com o Banco de Dados e o Google Sheets, transmitindo dados de maneira automática (Se houver internet).

<h1></h1>

<b><h4>MS5803xEME5803</h4></b>
O diretório **MS5803xEME5803** é onde está guardado o código de comparação entre dois barômetros, MS5803 e EME-BARO5803, que recebem os dados de Temperatura e Pressão.
O código tem a implementação com o Banco de Dados e o Google Sheets, transmitindo dados de maneira automática (Se houver internet).

<b><h4>SHT31xMS5803</h4></b>
O diretório **Sht31xMs5803** é onde está guardado o código de comparação entre os sensores SHT31 e MS5803, que recebem os dados de Temperatura e Umidade (sht31), e Temperatura e Pressão (Ms5803).
O código tem a implementação com o Banco de Dados e o Google Sheets, transmitindo dados de maneira automática (Se houver internet).

<h1></h1>

<b><h4>BKP_TXT</h4></b>
Todos os códigos aqui encontrados possuem a função de escrever esses dados recebidos em arquivos backup.txt, sendo eles:
- *SEC_BACKUP.TXT* -> Escreve de 5 em 5 segundos a leitura realizada pelos sensores (Bom para monitoramento).
- *HOUR_BACKUP.TXT* -> Escreve de 1 em 1 hora a leitura realizada pelos sensores.
- *DAY_BACKUP.TXT* -> Escreve de 1 em 1 dia (24 horas) a leitura realizada pelos sensores
O diretório **Bkp-txt** é onde estão guardados os relatórios .txt, que foram gravados durante os testes dos sensores em Temperatura ambiente, frio e calor.
*Necessário mudar caminho dos arquivos .TXT para que possam ser gravados corretamente*

<h1></h1>
