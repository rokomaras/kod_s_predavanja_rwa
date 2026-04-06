# Označava "services" kao Python paket.
# Ovdje živi POSLOVNA LOGIKA — pravila koja nemaju veze s HTTP-om.
# Service ne zna za Request/Response, samo za domenske objekte.
# Primjer (dolazi u predavanju 6):
#   def can_register(competition, now) -> bool:
#       return competition.prelim_deadline > now
