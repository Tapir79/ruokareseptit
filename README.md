# Ruokareseptit

* Sovelluksessa käyttäjät pystyvät jakamaan ruokareseptejään. Reseptissä lukee tarvittavat ainekset ja valmistusohje. []
* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen. [X]
* Käyttäjä pystyy lisäämään reseptejä ja muokkaamaan ja poistamaan niitä. [X]
* Käyttäjä näkee kaikki sovellukseen lisätyt reseptit. [X]
* Käyttäjä pystyy etsimään reseptejä hakusanalla. []
* Käyttäjäsivu näyttää, montako reseptiä käyttäjä on lisännyt ja listan käyttäjän lisäämistä resepteistä. []
* Käyttäjä pystyy valitsemaan reseptille yhden tai useamman luokittelun (esim. alkuruoka, intialainen, vegaaninen). []
* Käyttäjä pystyy suodattamaan reseptejä luokittelun perusteella. []
* Käyttäjä pystyy suodattamaan ja järjestämään reseptejä arvosanan perusteella. []
* Käyttäjä pystyy antamaan reseptille kommentin ja arvosanan. Reseptistä näytetään kommentit ja keskimääräinen arvosana. []
* Käyttäjä voi lisätä kuvan reseptiin []


# Sovelluksen asennus
Asenna `flask`-kirjasto:

``$ pip install flask``

Luo tietokannan taulut ja lisää alkutiedot: 
````
$ sqlite3 database.db < schema.sql
$ sqlite3 database.db < init.sql 
````

Voit käynnistää sovelluksen näin: 
`` $ flask run `` 
