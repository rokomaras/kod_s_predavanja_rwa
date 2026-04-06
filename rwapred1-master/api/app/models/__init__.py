# Označava "models" kao Python paket.
# Ovdje žive SQLAlchemy ORM modeli — Python klase koje predstavljaju
# tablice u bazi podataka.
# Primjer (dolazi u predavanju 2):
#   class User(Base):
#       __tablename__ = "users"
#       id = Column(Integer, primary_key=True)
#       email = Column(String, unique=True)
