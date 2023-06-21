# Rest Api

base url: `https://www.animeworld.so/api/`

<details>
    <summary><code>POST search/v2?keyword={keyword}</code></summary>

> Ricerca anime nel sito in base ad una chiave di ricerca.

- parametri:
    - `keyword`: chiave di ricerca
- header:
    - `csrf-token`: token cross-site request forgery

</details>
<br>
<details>
    <summary><code>POST download/{epID}</code></summary>

> Ottiene informazioni per il download dell'episodio richiesto.

- parametri:
    - `epID`: id episodio
- header:
    - `csrf-token`: token cross-site request forgery

</details>