from model.disc import Disc
class DiscService:
    def __init__(self, database):
        self.database = database

    def get_discs(self, args_dict):
        query = "SELECT discName, artist, releaseYear, musicStyle, availableQuantity, unitaryValue FROM disc"
        possible_keys = ['artist', 'discName', 'releaseYear', 'musicStyle']
        args_dict = {k: v for k, v in args_dict.items() if k in possible_keys}
        if len(args_dict) > 0:
            query += " WHERE "
            for key, value in args_dict.items():
                query += "LOWER({}) = LOWER('{}') AND ".format(key, value)
            query = query[:-4]
        self.database.query(query)
        rows = self.database.cur.fetchall()
        if rows is None:
            return None
        discs = []
        for row in rows:
            disc = Disc(row[0], row[1], row[2], row[3], row[4], row[5])
            discs.append(disc)
        return discs

    def get_discs_by_artist(self, artist):
        query = "SELECT discName, artist, releaseYear, musicStyle, availableQuantity, unitaryValue FROM disc WHERE LOWER(artist) = LOWER('{}')".format(artist)
        self.database.query(query)
        rows = self.database.cur.fetchall()
        if rows is None:
            return None
        discs = []
        for row in rows:
            disc = Disc(row[0], row[1], row[2], row[3], row[4], row[5])
            discs.append(disc)
        return discs

    def get_disc_by_artist_and_name(self, artist, discName):
        query = "SELECT discName, artist, releaseYear, musicStyle, availableQuantity, unitaryValue FROM disc WHERE LOWER(artist) = LOWER('{}') AND LOWER(discName) = LOWER('{}')".format(
            artist, discName)
        self.database.query(query)
        row = self.database.cur.fetchone()
        if row is None:
            return None
        disc = Disc(row[0], row[1], row[2], row[3], row[4], row[5])
        return disc

    def create_disc(self, disc):
        query = "INSERT INTO disc (discName, artist, releaseYear, musicStyle, availableQuantity, unitaryValue) VALUES ('{}', '{}', '{}', '{}', '{}', '{}')".format(
            disc.discName, disc.artist, disc.releaseYear, disc.musicStyle, disc.availableQuantity, disc.unitaryValue)
        self.database.query(query)
        self.database.commit()
        return disc

    def update_disc_quantity(self, artist, discName, quantityPurchased):
        query = "UPDATE disc SET availableQuantity = availableQuantity - {} WHERE LOWER(artist) = LOWER('{}') AND LOWER(discName) = LOWER('{}')".format(
            quantityPurchased, artist, discName)
        self.database.query(query)
        self.database.commit()
        if self.database.cur.rowcount == 0:
            return None
        return self.get_disc_by_artist_and_name(artist, discName)
