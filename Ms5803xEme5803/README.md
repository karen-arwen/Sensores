# MS5803 x EME5803
<table>
 <tr>
  <td>   
    <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTEAnJ29exhYAwGashW_eJUodFbDI3EbSVMww&s" width=200px height=200px display=inline-block>
    <br>
  </td>
  <td>
   <img src="https://camo.githubusercontent.com/f8d3d0ae49ce490eb587555cd9b9a571f3e5d6930458a233c5a360238d71d0df/68747470733a2f2f7777772e6167736f6c76652e636f6d2e62722f696d6770726f6475746f732f696d6167656e732f313134315f312e6a7067"  width=200px height=200px display=inline-block>
   <br>
  </td>
 </tr>
</table>
<h1></h1>

<b><h4>MS5803xEME5803</h4></b>
O diretório <b>Ms5803xEme5803</b> é onde está guardado o código de comparação entre dois barômetros, MS5803 e EME-BARO5803, que recebem os dados de Temperatura e Pressão.
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

<b><a href="https://docs.google.com/spreadsheets/d/1SGZZpKz5pi_VbSsaPf0dKUduC9N0vpDbYeVuPAUkeIw/edit?usp=sharing">Calor Seg</a></b> <br>
<b><a href="https://docs.google.com/spreadsheets/d/1nqEOixUd2SMpFiVatX9GmUTpkB-PukzNLfJfHUw6iV4/edit?usp=sharing">Calor Hora</a></b> <br> <br>

<h3>Frio</h3>
<b><a href="https://docs.google.com/spreadsheets/d/1s3CgjeUak83TciMwGSUQeP0BmFuSU1OcaexfAT6kvXM/edit?usp=sharing">Frio Seg</a></b> <br>
<b><a href="https://docs.google.com/spreadsheets/d/1Qut2fdeLmvm7cQzyWFdjrIVySn3M2wW1uk92Gv363WI/edit?usp=sharing">Frio Hora</a></b> <br>

<b><a href="https://docs.google.com/spreadsheets/d/14NaB-5sfpUzhf_lPtIyPwqeEIV_ZjIsppzxG3wfSMm8/edit?usp=sharing">Dashboard Geral</a></b> <br>



<h1></h1>
<h5>Importante!!</h5> 

Todos os códigos aqui encontrados possuem a função de escrever esses dados recebidos em arquivos backup.txt, sendo eles:
- *SEC_BACKUP.TXT* -> Escreve de 5 em 5 segundos a leitura realizada pelos sensores (Bom para monitoramento).
- *HOUR_BACKUP.TXT* -> Escreve de 1 em 1 hora a leitura realizada pelos sensores.
- *DAY_BACKUP.TXT* -> Escreve de 1 em 1 dia (24 horas) a leitura realizada pelos sensores
 
*Necessário mudar caminho dos arquivos .TXT para que possam ser gravados corretamente*
<h1></h1>

