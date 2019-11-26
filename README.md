<!-- ![LOGO](/RimborsiApp/static/RimborsiApp/imgs/missioni_logo.png?raw=true) -->

<p align="center">
  <a href="https://missioni.ing.unimore.it"><img src="/RimborsiApp/static/RimborsiApp/imgs/missioni_logo.png" width="300"></a>
</p>

# Rimborso Missioni UNIMORE

<p align="justify">L'applicazione è disponibile a <a href="https://missioni.ing.unimore.it">missioni.ing.unimore.it</a> ed è accessibile anche all'esterno del dipartimento di Ingegneria "Enzo Ferrari". L'autenticazione avviene mediante shibboleth quindi non è richiesta alcuna registrazione. Enjoy!</p>

# News
<p align="justify"><b>26/11/2019</b> - Possibilità di concludere (archiviare) una missione già rimborsata.</p>
<p align="justify"><b>26/11/2019</b> - E' stata aggiunta la possibilità di specificare valute diverse dall'euro. Il tasso di cambio      è quello fornito dalla <a href="https://tassidicambio.bancaditalia.it">Banca d'Italia</a> alla data in cui è stata effettuata la spesa (come indicato nel regolamento).</p>
<p align="justify"><b>26/11/2019</b> - Possibilità di clonare una missione esistente. </p>
<p align="justify"><b>20/08/2019</b> - Autocompilazione modulo kasko attiva! Per poter usufruire del servizio è necessario, nell'ordine, installare
il plugin del browser Tampermonkey e installare <a href="https://raw.githubusercontent.com/prittt/missioni-unimore/master/autocompilatore_richieste_kasko.user.js">questo</a> script. Fatto ciò,
quando cliccate sul link "kasko" nel resoconto missione si aprirà la pagina kasko di unimore con un pulsante speciale (Auto fill data from Tampermonkey storage).
Non vi resta che creare una nuova entry e cliccare sul pulsante magico!</p>
<p><b>19/08/2019</b> - Autocompilazione profilo utente con dati Shibboleth attiva.</p>

# Cosa pianifichiamo di aggiungere:

1. <p align="justify">Calcolo automatico dei km percorsi a mezzo macchina utilizzando API di qualche tipo. Purtroppo quelle di Via Michelin sono a pagamento e quelle di google "sottostimano" i km totali;</p>
1. <p align="justify">Calcolo del rimborso chilometrico come da regolamento. Attualmente vengono presi i dati dei prezzi benzina dell'ultima settimana (e non quelli della settimana missione) da <a href="https://dgsaie.mise.gov.it/prezzi_carburanti_settimanali.php?lang=it_IT">qui</a>, quindi non si dovrebbe discostare di molto da quello reale. Questa feature serve solamente per stimare il totale e verificare la correttezza del rimborso in quanto i calcoli finali verranno in ogni caso fatti dall'amministrazione.</p>
1. <p align="justify">Autocompletamento dati scontrini da foto (con relativa app smartphone) :metal:</p>

# Suggerimenti/Contributi?

<p align="justify">Chi vuole può contribuire allo sviluppo facendo pull request su questo repo o aprendo issue per richiedere nuove funzionalità o segnalare eventuali bug.</p>
