# =============================================================
# security.py — Hashiranje i verifikacija lozinki
# =============================================================
# Koristimo bcrypt direktno (ne passlib wrapper) jer passlib
# ima problem kompatibilnosti s bcrypt>=4.1.
#
# bcrypt automatski generira salt i ugrađuje ga u hash,
# pa ne moramo spremati salt odvojeno.
# =============================================================

import bcrypt


def hash_password(plain: str) -> str:
    """Hashira lozinku s bcrypt algoritmom. Vraća string spreman za bazu."""
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()


def verify_password(plain: str, hashed: str) -> bool:
    """Provjerava podudara li se plain lozinka s hashom iz baze."""
    return bcrypt.checkpw(plain.encode(), hashed.encode())
