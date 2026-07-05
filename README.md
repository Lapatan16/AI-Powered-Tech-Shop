# AI Powered Tech Shop

AI Powered Tech Shop je web aplikacija namenjena kupovini i prodaji bele tehnike. Projekat je razvijen u okviru predmeta **WEB2**, sa ciljem da se klasična online prodavnica unapredi korišćenjem veštačke inteligencije.

Glavna ideja projekta je da prodavcima olakša postavljanje oglasa. Nakon što daju kratak opis proizvoda, aplikacija koristi **Google Gemini** kako bi automatski predložila naziv proizvoda, opis, cenu i ostale informacije. Prodavac može da prihvati predlog ili da podatke izmeni ručno.

Kupcima je omogućena pretraga proizvoda, dodavanje proizvoda u korpu, kupovina, kao i dobijanje preporuka proizvoda na osnovu prethodnih aktivnosti.

---

# Glavne funkcionalnosti

### Autentifikacija korisnika

* Registracija i prijava korisnika
* JWT autentifikacija
* Zaštićene rute

### Upravljanje proizvodima

* Dodavanje proizvoda
* Izmena postojećih proizvoda
* Brisanje proizvoda
* Pregled svih proizvoda
* Pretraga proizvoda
* Kategorije proizvoda
* Upload slika proizvoda

### AI podrška

* Automatsko generisanje naziva proizvoda
* Generisanje opisa proizvoda
* Predlog cene
* Popunjavanje ostalih informacija
* Integracija sa Google Gemini API-jem

### Kupovina

* Dodavanje proizvoda u korpu
* Izmena sadržaja korpe
* Kreiranje porudžbina
* Pregled porudžbina

### Preporuke proizvoda

Sistem generiše preporuke proizvoda na osnovu aktivnosti korisnika, odnosno njegove istorije kupovine i korišćenja aplikacije.

---

# Korišćene tehnologije

## Backend

* Python
* FastAPI
* PostgreSQL
* Alembic
* Google Gemini API
* JWT autentifikacija

## Frontend

* React
* Vite
* JavaScript
* CSS

---

# Struktura projekta

```
AI-Powered-Tech-Shop
│
├── backend
│   ├── alembic
│   ├── src
│   ├── static
│   └── main.py
│
└── frontend
    ├── src
    ├── public
    └── package.json
```

Backend je organizovan po slojevima (API, servisi, repozitorijumi i modeli), dok frontend koristi React aplikaciju razvijenu pomoću Vite-a.

---

# Pokretanje projekta

## Potrebni alati

Pre pokretanja projekta potrebno je instalirati:

* Python 3.14+
* Node.js
* PostgreSQL
* Git

---

# Kloniranje projekta

```bash
git clone https://github.com/Lapatan16/AI-Powered-Tech-Shop.git

cd AI-Powered-Tech-Shop
```

---

# Podešavanje baze

Potrebno je napraviti PostgreSQL bazu pod nazivom:

```
ai-powered-tech-shop-db
```

Nakon toga izvršiti Alembic migracije.

```bash
alembic upgrade head
```

---

# Backend

Ući u backend direktorijum.

```bash
cd backend
```

Napraviti `.env` fajl.

Primer sadržaja:

```env
DB_CONNECTION="postgresql+asyncpg://postgres:password@localhost:5432/ai-powered-tech-shop-db"
MIGRATION_DB_CONNECTION="postgresql+psycopg2://postgres:password@localhost:5432/ai-powered-tech-shop-db"

JWT_SECRET_KEY="your-secret-key"
JWT_ALGORITHM="HS256"
JWT_ACCESS_TOKEN_EXPIRE_MINUTES="30"

GEMINI_API_KEY="your-api-key"
```

Instalacija zavisnosti:

```bash
pip install -r requirements.txt
```

Pokretanje backend-a:

```bash
python main.py
```

Backend će biti dostupan na:

```
http://localhost:9061
```

Swagger dokumentacija:

```
http://localhost:9061/docs
```

---

# Frontend

Otvoriti novi terminal.

```bash
cd frontend
```

Napraviti `.env` fajl.

```env
VITE_API_BASE_URL="http://localhost:9061"
```

Instalacija paketa:

```bash
npm install
```

Pokretanje aplikacije:

```bash
npm run dev
```

Frontend će biti dostupan na adresi koju Vite ispiše u terminalu (najčešće http://localhost:5173).

---

# Slike proizvoda

Sve slike koje korisnici otpreme čuvaju se lokalno u direktorijumu:

```
backend/static/uploads
```

Frontend automatski preuzima slike sa backend-a, tako da nije potrebno dodatno podešavanje.

---

# Google Gemini

Za korišćenje AI funkcionalnosti potrebno je posedovati **Google Gemini API ključ**.

API ključ se unosi u backend `.env` fajl kroz promenljivu:

```env
GEMINI_API_KEY="your-api-key"
```

Bez ovog ključa AI funkcionalnosti neće raditi.

---

# Arhitektura

Backend je organizovan korišćenjem višeslojne arhitekture.

Projekat koristi:

* Repository pattern
* Service layer
* Unit of Work pattern
* JWT autentifikaciju
* Asinhroni pristup bazi podataka
* Pozadinske radnike za obradu preporuka

Ovakva organizacija omogućava lakše održavanje i proširenje aplikacije.

---

# Buduća unapređenja

Neke od mogućih nadogradnji projekta:

* Deploy aplikacije
* Naprednije preporuke proizvoda
* Više AI funkcionalnosti
* Notifikacije korisnicima
* Ocene i komentari proizvoda
* Plaćanje putem eksternih servisa

---

# Autor

Projekat je razvijen u okviru predmeta **WEB2**.

Autor: **Mateja Lapatanović**
