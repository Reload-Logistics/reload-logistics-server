NO = False
YES = True
YES_NO_CHOICES = [(NO, "NO"), (YES, "YES")]
RATING = [(rating, rating) for rating in range(1, 6)]
PAYMENTOPTIONS = [("EFT", "EFT"), ("CASH", "CASH")]
FLOORSCHOICES = [(floor, floor) for floor in range(12)]
HELPERCHOICES = [(helper + 1, helper + 1) for helper in range(3)]
VEHICLESIZECHOICES = [(1.0, "1 Ton"), (1.5, "1.5 Ton"), 
                      (2.0, "2 Ton"), (3.0, "3 Ton"), 
                      (8.0, "8 Ton")]

website_url = "https://matols.co.za"