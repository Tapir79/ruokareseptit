# Ruokareseptit

[X] = toteutettu      

* Sovelluksessa käyttäjät pystyvät jakamaan ruokareseptejään. Reseptissä lukee tarvittavat ainekset, kuvaus ja valmistusohje. [X]
* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen. [X]
* Käyttäjä pystyy lisäämään reseptejä ja muokkaamaan ja poistamaan niitä. [X]
* Käyttäjä pystyy lisäämään reseptiin aineisosia, muokkaamaan ja poistamaan niitä. [X]
* Käyttäjä pystyy lisäämään reseptiin ohjeita, muokkaamaan ja poistamaan niitä. [X]
* Käyttäjä näkee kaikki sovellukseen lisätyt reseptit. [X]
* Käyttäjä pystyy etsimään reseptejä hakusanalla. [X]
* Käyttäjä pystyy valitsemaan reseptille yhden tai useamman luokittelun (esim. alkuruoka, intialainen, vegaaninen). [X]
* Käyttäjä pystyy suodattamaan reseptejä luokittelun perusteella. []
* Käyttäjä pystyy antamaan reseptille kommentin [X]
* Reseptistä näytetään kommentit [X]
* Käyttäjä pystyy antamaan reseptille arvosanan. [X]
* Reseptistä näytetään keskimääräinen arvosana. []
* Käyttäjä pystyy suodattamaan ja järjestämään reseptejä arvosanan perusteella. []
* Käyttäjä voi lisätä kuvan reseptiin []
* Käyttäjäsivu näyttää, montako reseptiä käyttäjä on lisännyt ja listan käyttäjän lisäämistä resepteistä. [X]
* Sovelluksella on CSS-tyylitiedosto [x]


# Sovelluksen asennus
Asenna `flask`-kirjasto:

``$ pip install flask``

Luo tietokannan taulut ja lisää alkutiedot: 
````
$ sqlite3 database.db < schema.sql
````

Voit käynnistää sovelluksen näin: 
`` $ flask run `` 
