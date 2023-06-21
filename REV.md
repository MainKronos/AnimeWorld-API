# Rest Api

base url: `https://www.animeworld.so/api/`

## Anonimo

> Richieste che non richiedono di essere autenticati.

### POST

<details>
    <summary><code>POST search/v2?keyword={keyword}</code></summary>

> Ricerca anime nel sito in base ad una chiave di ricerca.

- parametri:
    - `keyword`: chiave di ricerca
- header:
    - `csrf-token`: token cross-site request forgery

</details>

<details>
    <summary><code>POST download/{epID}</code></summary>

> Restituisce informazioni per il download dell'episodio richiesto.

- parametri:
    - `epID`: id episodio
- header:
    - `csrf-token`: token cross-site request forgery

</details>

<details>
    <summary><code>POST comments/anime/get/{animeID}</code></summary>

> Restituisce i commenti degli utenti dell'anime selezionato.

> **Warning**\
> Restituisce una risposta in formato HTML.

- parametri:
    - `animeID`: id anime 
    - `epID`: id episodio
- header:
    - `csrf-token`: token cross-site request forgery

</details>

<details>
    <summary><code>POST comments/anime/get/{animeID}/{epID}</code></summary>

> Restituisce i commenti degli utenti di un episodio dell'anime selezionato.

> **Warning**\
> Restituisce una risposta in formato HTML.

- parametri:
    - `animeID`: id anime 
    - `epID`: id episodio
- header:
    - `csrf-token`: token cross-site request forgery

</details>

<details>
    <summary><code>POST user/register</code></summary>

> Registra un account sul sito.

> **Note**\
> In caso di successo restituisce un codice 302.

- payload:
    - `_csrf:`: token cross-site request forgery
    - `username`: nome utente
    - `email`: email
    - `password`: password
    - `confirmPassword`: password di conferma
    - `g-recaptcha-response:`: token captcha

</details>

### GET

<details>
    <summary><code>GET tooltip/{animeID}</code></summary>

> Restituisce informazioni generali e **sintetiche** sull'anime.

> **Warning**\
> Restituisce una risposta in formato HTML.

- parametri:
    - `animeID`: id anime
- header:
    - `csrf-token`: token cross-site request forgery

</details>

<details>
    <summary><code>GET schedule?time={timestamp}</code></summary>

> Restituisce il calendario delle uscite degli episodi per il giorno indicato.

> **Warning**\
> Restituisce una risposta in formato HTML.

- parametri:
    - `timestamp`: timestamp in millisecondi con timezone GMT+2

</details>

## Utente

> Richieste che richiedono di essere autenticati.

### POST

<details>
    <summary><code>POST comments/profile/post/{userID}</code></summary>

> Restituisce informazioni su una notifica ricevuta.

- parametri:
  - `userID`: id utente
- payload:
  - `comment`: commento
- coockie:
  - `sessionId`: token di sessione
- header:
  - `csrf-token`: token cross-site request forgery

</details>

### GET

<details>
    <summary><code>GET notifications/open/{notificationID}</code></summary>

> Restituisce informazioni su una notifica ricevuta.

- parametri:
    - `notificationID`: id notifica
- coockie:
    - `sessionId`: token di sessione

</details>