# Ruokareseptit

## Sisällysluettelo

- [Sovelluksen asennus](#sovelluksen-asennus)
  - [Asenna `flask`-kirjasto](#asenna-flask-kirjasto)
  - [Luo tietokanta](#luo-tietokanta)
  - [(Optionaalinen) lisää testidata tietokantaan](#optionaalinen-lisaa-testidata-tietokantaan)
  - [Käynnistä sovellus](#käynnista-sovellus)
- [Toteutukset](#toteutukset)
  - [Toiminnallisuudet](#toiminnallisuudet)
  - [Tekniset perusvaatimukset](#tekniset-perusvaatimukset)
  - [Toimivuus](#toimivuus)
  - [Versionhallinta](#versionhallinta)
  - [Ohjelmointityyli](#ohjelmointityyli)
  - [Tietokanta-asiat](#tietokanta-asiat)
  - [Sovelluksen turvallisuus](#sovelluksen-turvallisuus)
  - [Suuren tietomäärän käsittely](#kuormitustestaus)

---

# Sovelluksen asennus

## Asenna `flask`-kirjasto

`$ pip install flask`

## Luo tietokanta

Aja skripti, joka asentaa tietokannan (ja testidataa) automaattisesti:

`$ . install.sh`

Jos automaattiasennus ei toimi, voit tehdä asennuksen myös manuaalisesti:

Luo tietokannan taulut ja lisää alkutiedot:

```
$ sqlite3 database.db < install/schema.sql
$ sqlite3 database.db < install/init.sql
```

## Testidata tietokantaan

Aja tietokantaan valmista testidataa:

```
$ sqlite3 database.db < install/test_data.sql
$ python install/upload_images.py
```

Testidata sisältää yhden valmiin reseptin ja arvostelun reseptille.  
Lisäksi luodaan 2 valmista testikäyttäjää:

| Tunnus   | Salasana |
| -------- | -------- |
| guybrush | guybrush |
| elaine   | elaine   |

## Käynnistä sovellus

`$ flask run`

---

# Toteutukset

## Toiminnallisuudet

- [X] Sovelluksessa käyttäjät pystyvät jakamaan ruokareseptejään. Reseptissä lukee tarvittavat ainekset, kuvaus ja valmistusohje.
- [X] Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
- [X] Käyttäjä pystyy lisäämään reseptejä ja muokkaamaan ja poistamaan niitä.
- [X] Käyttäjä pystyy lisäämään reseptiin aineisosia, muokkaamaan ja poistamaan niitä.
- [X] Käyttäjä pystyy lisäämään reseptiin ohjeita, muokkaamaan ja poistamaan niitä.
- [X] Käyttäjä näkee kaikki sovellukseen lisätyt reseptit.
- [X] Käyttäjä pystyy etsimään reseptejä hakusanalla.
- [X] Käyttäjä pystyy valitsemaan reseptille yhden tai useamman luokittelun (esim. alkuruoka, intialainen, vegaaninen).
- [X] Käyttäjä pystyy antamaan reseptille kommentin.
- [X] Reseptistä näytetään kommentit.
- [X] Käyttäjä pystyy antamaan reseptille arvosanan.
- [X] Reseptistä näytetään keskimääräinen arvosana.
- [X] Käyttäjä pystyy suodattamaan reseptejä ruokavalioluokittelun perusteella.
- [X] Käyttäjä pystyy suodattamaan reseptejä ruokakulttuuriluokittelun perusteella.
- [X] Käyttäjä pystyy suodattamaan reseptejä arvosanan perusteella.
- [X] Käyttäjä pystyy järjestämään reseptejä arvosanan perusteella.
- [X] Käyttäjä pystyy järjestämään reseptejä otsikon perusteella.
- [X] Käyttäjä voi lisätä kuvan reseptiin.
- [X] Käyttäjäsivu näyttää, montako reseptiä käyttäjä on lisännyt ja listan käyttäjän lisäämistä resepteistä.
- [X] Sovelluksella on CSS-tyylitiedosto.

## Tekniset perusvaatimukset

- [X] Sovellus on pyritty toteuttamaan mahdollisiman tarkasti kurssimateriaalia seuraten
- [X] Sovellus toteutettu Pythonilla käyttäen Flask-kirjastoa
- [X] Sovellus käyttää SQLite-tietokantaa
- [X] Kehitystyössä käytetty Gitiä ja GitHubia
- [X] Sovelluksen käyttöliittymä muodostuu HTML-sivuista
- [X] Sovelluksessa ei ole käytetty JavaScript-koodia
- [X] Tietokantaa käytetään suoraan SQL-komennoilla (ei ORMia)
- [X] Kirjaston flask lisäksi käytössä ei muita erikseen asennettavia kirjastoja

## Toimivuus

- [X] Käyttäjän lähettämässä tekstissä rivinvaihdot näkyvät selaimessa (kuvausteksti)
- [X] Kuvissa käytetty alt-attribuuttia (jos sovelluksessa kuvia)
- [X] Lomakkeissa käytetty label-elementtiä
- [X] CSS:n avulla toteutettu ulkoasu

## Versionhallinta

- [X] Kehitystyön aikana on tehty commiteja säännöllisesti
- [X] Commit-viestit on kirjoitettu englanniksi
- [X] Commitit on pyritty pilkkomaan siten, että ne koskevat tiettyä kokonaisuutta
- [X] Commit-viesteissä pyritty noudattamaan kurssin tyyliä ja näitä yleisiä hyviä käytäntöjä: https://www.freecodecamp.org/news/how-to-write-better-git-commit-messages/
- [X] Versionhallinnasta pyritty poistamaan kaikki sinne kuulumattomat tiedostot
- [X] README.md pyritty laatimaan mahdollisimman kuvaavaksi

## Ohjelmointityyli

- [X] Ajettu pylint ja korjattu koodia sen mukaisesti
- [X] Koodi automaattityylitelty Pythonin Black formatteria käyttäen, joka taas noudattaa pylintin suosituksia
- [X] Sisennyksen leveys on neljä välilyöntiä
- [X] Koodi on kirjoitettu englanniksi
- [X] Muuttujien ja funktioiden nimet muotoa total_count (snake_case)
- [X] Pythonin merkkijonoissa käytetty aina `"`
- [X] Pylintillä tarkistettu, että Välit oikein `=`-merkin ja `,`-merkin ympärillä
- [X] Kaikilla funktioilla on useita mahdollisia palautusarvoja
- [X] If- ja While- ehtojen ympärillä ei ole sulkeita
- [X] Ei seuraavankaltaisia ehtoja `result is None`

## Tietokanta-asiat

- [X] Taulut ja sarakkeet on nimetty englanniksi
- [X] Taulujen ja sarakkeiden nimeämisessä on pyritty noudattamaan hyviä käytäntöjä
- [X] Käytetty `REFERENCES`-määrettä, kun viittaus toiseen tauluun
- [X] Käytetty `UNIQUE`-määrettä, kun tulee olla eri arvo joka rivillä
- [X] Ei kyselyjä muotoa `SELECT *`
- [X] Pitkät SQL-komennot jaettu usealle riville
- [X] Kaikki tiedot pyritty hakemaan yhdellä SQL-kyselyllä, jos järkevästi mahdollista
- [X] Pyritty pitämään kiinni ohjeesta: Koodissa ei tehdä asioita, jotka voi mielekkäästi tehdä SQL:ssä
- [X] Käytetty try/except SQL-komennon ympärillä vain aiheellisesti

## Sovelluksen turvallisuus

- [X] Salasanat tallennetaan tietokantaan asianmukaisesti
- [X] Käyttäjän oikeus nähdä sivun sisältö tarkastetaan
- [X] Käyttäjän oikeus lähettää lomake tarkastetaan
- [X] Käyttäjän syötteet tarkastetaan ennen tietokantaan lisäämistä
- [X] SQL-komennoissa käytetty parametreja
- [X] Sivut muodostetaan sivupohjien kautta
- [X] Lomakkeissa on estetty CSRF-aukko

## Kuormitustestaus

Eli suuren tietomäärän käsittely

- [X] Sovellusta testattu suurella tietomäärällä ja raportoitu tulokset. [README_load_testing.md](https://github.com/Tapir79/ruokareseptit/blob/main/README_load_testing.md)
- [X] Sovelluksessa käytössä tietokohteiden sivutus
- [X] Tietokantaan lisätty indeksi, joka nopeuttaa suuren tietomäärän käsittelyä
