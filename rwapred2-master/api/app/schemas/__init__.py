# Označava "schemas" kao Python paket.
# Ovdje žive Pydantic modeli (DTO — Data Transfer Objects).
# Schema definira UGOVOR API-ja: što klijent šalje i što dobiva natrag.
# Primjer (dolazi u predavanju 5):
#   class LifterCreate(BaseModel):
#       first_name: str
#       last_name: str
#       birth_date: date
