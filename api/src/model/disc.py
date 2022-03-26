class Disc:
    def __init__(self, disc_name, artist, release_year, music_style, unitary_value, available_quantity):
        self.disc_name = disc_name
        self.artist = artist
        self.release_year = release_year
        self.music_style = music_style
        self.unitary_value = unitary_value
        self.available_quantity = available_quantity

    def __repr__(self):
        return "<Disc {}>".format(self.disc_name)