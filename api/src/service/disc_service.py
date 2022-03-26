import json
import sys
from model.disc import Disc


class DiscService:
    def __init__(self, database):
        self.database = database

    def get_discs(self):
        query = "SELECT * FROM disc"
        self.database.query(query)
        rows = self.database.cur.fetchall()
        if rows is None:
            return None
        discs = []
        for row in rows:
            disc = Disc(row[0], row[1], row[2], row[3], row[4], row[5])
            discs.append(disc)
        return json.dumps([ob.__dict__ for ob in discs])

    def get_disc_by_artist_and_name(self, disc_artist, disc_name):
        query = "SELECT * FROM disc WHERE artist = '{}' AND discName = '{}'".format(
            disc_artist, disc_name)
        self.database.query(query)
        row = self.database.cur.fetchone()
        if row is None:
            return None
        disc = Disc(row[0], row[1], row[2], row[3], row[4], row[5])
        return json.dumps(disc.__dict__)

    def create_disc(self, disc):
        query = "INSERT INTO disc (discName, artist, releaseYear, musicStyle, availableQuantity, unitaryValue) VALUES ('{}', '{}', '{}', '{}', '{}', '{}')".format(
            disc.disc_name, disc.artist, disc.release_year, disc.music_style, disc.available_quantity, disc.unitary_value)
        self.database.query(query)
        self.database.commit()
        return json.dumps(disc.__dict__)

    def update_disc_decrement_quantity(self, disc_artist, disc_name):
        query = "UPDATE disc SET availableQuantity = availableQuantity - 1 WHERE artist = '{}' AND discName = '{}'".format(
            disc_artist, disc_name)
        self.database.query(query)
        self.database.commit()
        if self.database.cur.rowcount == 0:
            return None
        return self.get_disc_by_artist_and_name(disc_artist, disc_name)
