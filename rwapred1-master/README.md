# Powerlifting Competition Registrations

Sustav za prijavu natjecatelja na powerlifting natjecanja.  
Projekt za kolegij **Razvoj web aplikacija** — SIT UNIZD.

---

## Tehnologije

| Sloj     | Stack                                  |
|----------|----------------------------------------|
| Backend  | Python 3.11+, FastAPI, SQLAlchemy 2.0  |
| Baza     | PostgreSQL 16 (Docker Compose)         |
| Frontend | Vue 3, Pinia, Vue Router (dolazi P7+)  |
| Auth     | JWT (access + refresh tokeni)          |

---

## Preduvjeti

Prije pokretanja projekta trebate imati instalirano:

- **Python** ≥ 3.11 — [python.org/downloads](https://www.python.org/downloads/)
- **Docker Desktop** — [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop/)
- **Git** — [git-scm.com](https://git-scm.com/)
- (Za frontend, od predavanja 7) **Node.js** ≥ 18

---

## Brzo pokretanje

### 1. Kloniraj repo i kopiraj env varijable

```bash
git clone <url>
cd <repo>

# Linux/macOS:
cp .env.example .env

# Windows (PowerShell):
Copy-Item .env.example .env
```

### 2. Pokreni PostgreSQL bazu

```bash
docker compose up -d db
```

Provjera da baza radi:
```bash
docker compose ps
# Status treba biti "healthy"
```

### 3. Pokreni backend (FastAPI)

```bash
cd api

# Kreiraj virtualno okruženje (jednom):
python -m venv .venv

# Aktiviraj ga:
# Linux/macOS:         source .venv/bin/activate
# Windows PowerShell:  .venv\Scripts\Activate.ps1
# Windows cmd:         .venv\Scripts\activate.bat

# Instaliraj zavisnosti:
pip install -r requirements.txt

# Pokreni dev server:
uvicorn app.main:app --reload
```

### 4. Provjera

- Health check: http://127.0.0.1:8000/health → `{"status": "ok"}`
- Swagger UI:   http://127.0.0.1:8000/docs

---

## Struktura projekta

```
repo/
├── api/                      # FastAPI backend
│   ├── app/
│   │   ├── main.py           # App factory — sastavlja aplikaciju
│   │   ├── core/             # Infrastruktura (config, errors, logging)
│   │   │   ├── config.py     # Pydantic Settings — čita env varijable
│   │   │   ├── errors.py     # AppError + globalni exception handler
│   │   │   ├── logging.py    # Konfiguracija logiranja
│   │   │   └── deps.py       # FastAPI dependencije (DB session, auth)
│   │   ├── routers/          # HTTP sloj — tanki routeri
│   │   ├── services/         # Poslovna logika (pravila, validacija)
│   │   ├── repositories/     # DB upiti (SQL, transakcije)
│   │   ├── models/           # SQLAlchemy ORM modeli (tablice)
│   │   └── schemas/          # Pydantic DTO-ovi (ulaz/izlaz API-ja)
│   ├── tests/
│   ├── requirements.txt
│   └── pyproject.toml
├── web/                      # Vue frontend (od predavanja 7)
├── docker-compose.yml        # PostgreSQL u kontejneru
├── .env.example              # Primjer env varijabli (IDE U GIT)
├── .gitignore
└── README.md
```

---

## Slojevi backend arhitekture

Svaki sloj ima jednu odgovornost. Pravilo: **gornji sloj može zvati donji, ali nikad obrnuto**.

```
  HTTP request
       ↓
  ┌─────────┐
  │ Router   │  Parsira request, poziva service, vraća HTTP response.
  └────┬─────┘  NE sadrži poslovnu logiku.
       ↓
  ┌─────────┐
  │ Service  │  Provodi poslovna pravila (rokovi, vlasništvo, validacija).
  └────┬─────┘  NE zna za HTTP status kodove.
       ↓
  ┌──────────────┐
  │ Repository   │  Izvršava SQL upite, vraća domenske objekte.
  └──────┬───────┘  NE zna za poslovnu logiku.
         ↓
  ┌─────────┐
  │   DB    │  PostgreSQL
  └─────────┘
```

| Sloj         | Odgovornost                              | Primjer datoteke         |
|--------------|------------------------------------------|--------------------------|
| Router       | HTTP: parsiranje requesta, status kodovi | `routers/health.py`      |
| Service      | Poslovna pravila, validacija, orkestra.  | `services/auth.py`       |
| Repository   | SQL upiti, transakcije                   | `repositories/user.py`   |
| Model        | ORM definicija tablica                   | `models/user.py`         |
| Schema (DTO) | Pydantic ulaz/izlaz modeli               | `schemas/user.py`        |

---

## Git konvencije

### Commit poruke

Format: `<tip>(<scope>): <opis>`

| Tip        | Značenje                             |
|------------|--------------------------------------|
| `feat`     | Nova funkcionalnost                  |
| `fix`      | Ispravka buga                        |
| `refactor` | Promjena bez nove funkcionalnosti    |
| `chore`    | Tooling, config, infrastruktura      |
| `docs`     | Dokumentacija                        |
| `test`     | Testovi                              |

Scope: `api`, `web`, ili prazan za root-level promjene.

### Env varijable

- Tajne (lozinke, JWT secret) **NIKAD** ne idu u git
- `.env.example` sadrži ključeve s demo vrijednostima — ide u git
- `.env` sadrži stvarne vrijednosti — **NE** ide u git (vidi `.gitignore`)
- U produkciji: env varovi dolaze iz platforme (Railway/Render)

---

## Korisne naredbe

```bash
# -- Baza --
docker compose up -d db          # Pokreni PostgreSQL
docker compose ps                # Status kontejnera
docker compose logs db           # Logovi baze
docker compose down              # Zaustavi sve
docker compose down -v           # Zaustavi + obriši podatke (reset)

# -- Backend --
uvicorn app.main:app --reload    # Dev server s auto-reloadom
pytest                           # Pokreni testove
ruff check .                     # Lint (provjera kvalitete koda)
black .                          # Format (automatsko formatiranje)

# -- Git --
git log --oneline --decorate     # Kratki pregled povijesti
git diff <commit1>..<commit2>    # Usporedba dva commita
git show <commit>                # Detalji jednog commita
```
