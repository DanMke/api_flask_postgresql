class Disc:
    def __init__(self, discName, artist, releaseYear, musicStyle, unitaryValue, availableQuantity):
        self.discName = discName
        self.artist = artist
        self.releaseYear = releaseYear
        self.musicStyle = musicStyle
        self.unitaryValue = unitaryValue
        self.availableQuantity = availableQuantity

    def __repr__(self):
        return "<Disc {}>".format(self.discName)