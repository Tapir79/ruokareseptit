# Ruokareseptit

[X] = toteutettu      

* [X] Sovelluksessa käyttäjät pystyvät jakamaan ruokareseptejään. Reseptissä lukee tarvittavat ainekset, kuvaus ja valmistusohje.
* [x]Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
* [x]Käyttäjä pystyy lisäämään reseptejä ja muokkaamaan ja poistamaan niitä.
* [x]Käyttäjä pystyy lisäämään reseptiin aineisosia, muokkaamaan ja poistamaan niitä.
* [x]Käyttäjä pystyy lisäämään reseptiin ohjeita, muokkaamaan ja poistamaan niitä.
* [x]Käyttäjä näkee kaikki sovellukseen lisätyt reseptit.
* [x]Käyttäjä pystyy etsimään reseptejä hakusanalla.
* [x]Käyttäjä pystyy valitsemaan reseptille yhden tai useamman luokittelun (esim. alkuruoka, intialainen, vegaaninen).
* []Käyttäjä pystyy suodattamaan reseptejä luokittelun perusteella.
* [x]Käyttäjä pystyy antamaan reseptille kommentin.
* [x]Reseptistä näytetään kommentit.
* [x]Käyttäjä pystyy antamaan reseptille arvosanan.
* [x]Reseptistä näytetään keskimääräinen arvosana.
* [x]Käyttäjä pystyy suodattamaan reseptejä arvosanan perusteella.
* []Käyttäjä pystyy järjestämään reseptejä arvosanan perusteella.
* [x]Käyttäjä voi lisätä kuvan reseptiin
* [x]Käyttäjäsivu näyttää, montako reseptiä käyttäjä on lisännyt ja listan käyttäjän lisäämistä resepteistä.
* [x]Sovelluksella on CSS-tyylitiedosto


# Sovelluksen asennus
Asenna `flask`-kirjasto:

``$ pip install flask``

Luo tietokannan taulut ja lisää alkutiedot: 
````
$ sqlite3 database.db < schema.sql
````

Voit käynnistää sovelluksen näin: 
`` $ flask run `` 
