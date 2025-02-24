# Ruokareseptit

[X] = toteutettu      

* [X] Sovelluksessa käyttäjät pystyvät jakamaan ruokareseptejään. Reseptissä lukee tarvittavat ainekset, kuvaus ja valmistusohje.
* [X]Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
* [X]Käyttäjä pystyy lisäämään reseptejä ja muokkaamaan ja poistamaan niitä.
* [X]Käyttäjä pystyy lisäämään reseptiin aineisosia, muokkaamaan ja poistamaan niitä.
* [X]Käyttäjä pystyy lisäämään reseptiin ohjeita, muokkaamaan ja poistamaan niitä.
* [X]Käyttäjä näkee kaikki sovellukseen lisätyt reseptit.
* [X]Käyttäjä pystyy etsimään reseptejä hakusanalla.
* [X]Käyttäjä pystyy valitsemaan reseptille yhden tai useamman luokittelun (esim. alkuruoka, intialainen, vegaaninen).
* [X]Käyttäjä pystyy antamaan reseptille kommentin.
* [X]Reseptistä näytetään kommentit.
* [X]Käyttäjä pystyy antamaan reseptille arvosanan.
* [X]Reseptistä näytetään keskimääräinen arvosana.
* [X]Käyttäjä pystyy suodattamaan reseptejä ruokavalioluokittelun perusteella.
* [X]Käyttäjä pystyy suodattamaan reseptejä ruokakulttuuriluokittelun perusteella.
* []Käyttäjä pystyy suodattamaan reseptejä arvosanan perusteella.
* []Käyttäjä pystyy järjestämään reseptejä arvosanan perusteella.
* [X]Käyttäjä voi lisätä kuvan reseptiin
* [X]Käyttäjäsivu näyttää, montako reseptiä käyttäjä on lisännyt ja listan käyttäjän lisäämistä resepteistä.
* [X]Sovelluksella on CSS-tyylitiedosto


# Sovelluksen asennus 

## Asenna `flask`-kirjasto:    
    ``$ pip install flask``

## Luo tietokanta
   
``$ . install.sh``

Jos automaattiasennus ei toimi, voit tehdä asennuksen myös manuaalisesti:

Luo tietokannan taulut ja lisää alkutiedot: 
````
$ sqlite3 database.db < schema.sql
$ sqlite3 database.db < init.sql
````

## (Optionaalinen) lisää testidata tietokantaan

Aja tietokantaan valmista testidataa:
````
$ sqlite3 database.db < test_data.sql
````

Testidata sisältää yhden valmiin reseptin ja arvostelun reseptille.    
Lisäksi luodaan 2 valmista testikäyttäjää:

|tunnus|salasana|
|-|-|
|guybrush|guybrush|
|elaine|elaine|

## Käynnistä sovellus    
`` $ flask run ``


