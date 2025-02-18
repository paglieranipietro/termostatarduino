# termostatarduino


https://github.com/user-attachments/assets/34ae72cd-3ddf-4261-9f9f-b363b3836a29


``termostarduino`` é un progetto che mira all'analisi di umiditá e temperatura dell'ambiente circostante.

Tramite una scheda di prototipazione Arduino ed un sensore `DHT11`, termostarduino realizzerá
degli accattivanti grafici tramite l'utilizzo della libreria grafica `dearpigui`.

I dati raccolti in tempo d'esecuzione verranno poi salvati in un file json per una successiva analisi dell'utilizzatore qualora quest'ultimo lo necessiti.

## Componenti necessari

1. Una scheda `arduino` (qualsiasi é utilizzabile, purché disponga di almeno 3 pin digitali e di due pin per l'alimentazione a 5V)
2. Un sensore `DHT11`
3. Due LED

## Montaggio del circuito

![circuito](https://github.com/user-attachments/assets/14e24e45-8cac-4a37-8b22-eb65f64035ff)

N.B.: Il pinout del DHT11 potrebbe variare in base al produttore, verificare dal datasheet fornito dal produttore per evitare guasti.

## Dipendenze

### Arduino
Le librerie da installare all'interno dell'Arduino IDE sono `DHT11.h` e `ArduinoJson.hpp`

### Python
Le librerie, installabili tramite `pip`, sono `pyserial`, `screeninfo` e `dearpigui`


## Come installare ed utilizzare termostarduino

1. Per prima cosa installare le dipendenze necessarie tramite `pip` e nell'Arduino IDE
2. Effettuare un `git clone` di questa repository all'interno di una cartella vuota
3. Aprire il file `termostarduino_dht11/termostarduino_dht11.ino` all'interno di Arduino IDE e caricarlo all'interno di una scheda Arduino compatibile
4. Mentre la scheda é collegata al computer, eseguire `main.py`

Una volta inserito il numero di porta COM virtuale a cui si é collegata la scheda Arduino, sará possibile visionare i grafici di Umiditá e Temperatura nel tempo, oltre ad uno specchietto che riferisce l'attuale stato dei LED

## Personalizzazione

All'interno del file `termostarduino_dht11/termostarduino_dht11.ino` é possibile modificare una serie di parametri:

- Le costanti `LED1` e `LED2`, che indicano rispettivamente a quale pin sono collegati i LED verde e rosso
- Il pin a cui é collegato il sensore `DHT11` (all'interno del costruttore dell'oggetto `sensore`)
- Le soglie minima e massima al superamento delle quali verranno accesi i LED (`SOGLIA_MINIMA` e `SOGLIA_MASSIMA`)
- Ogni quanti ms inviare i dati raccolti dal sensore alla seriale per l'elaborazione e la visualizzazione nel programma principale (`SEND_INTERVAL`)

## Presentazione

È stata ralizzata una presentazione che spiega le idee relative a questo progetto

[Presentazione canva](https://www.canva.com/design/DAGe45uReeU/z94VznGvpwEeyN7mJQWm8w/edit?utm_content=DAGe45uReeU&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)



