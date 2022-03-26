from flask import jsonify, request
import json
from model.disc import Disc
from service.disc_service import DiscService

class DiscController:
    def __init__(self, app, database):
        self.app = app
        self.disc_service = DiscService(database)
        self.routes()

    def routes(self):
        @self.app.route('/discs', methods=['GET'])
        def get_discs():
            args = request.args
            discs = self.disc_service.get_discs(args.to_dict())
            if discs is None:
                return [], 200
            return json.dumps([ob.__dict__ for ob in discs]), 200

        @self.app.route('/discs/<disc_artist>/', methods=['GET'])
        def get_discs_by_artist(disc_artist):
            discs = self.disc_service.get_discs_by_artist(disc_artist)
            if discs is None:
                return jsonify({'message': 'Disc not found'}), 404
            return json.dumps([ob.__dict__ for ob in discs]), 200

        @self.app.route('/discs/<disc_artist>/<discName>', methods=['GET'])
        def get_disc_by_artist_and_name(disc_artist, discName):
            disc = self.disc_service.get_disc_by_artist_and_name(disc_artist, discName)
            if disc is None:
                return jsonify({'message': 'Disc not found'}), 404
            return json.dumps(disc.__dict__), 200

        @self.app.route('/discs', methods=['POST'])
        def create_disc():
            if not request.json:
                return jsonify({'message': 'No data provided'}), 400
            elif (
                'artist' not in request.json or 'discName' not in request.json or 
                'releaseYear' not in request.json or 'musicStyle' not in request.json or 
                'unitaryValue' not in request.json or 'availableQuantity' not in request.json or 
                not request.json['discName'] or not request.json['artist'] or 
                not request.json['releaseYear'] or not request.json['musicStyle'] or 
                not request.json['unitaryValue']or not request.json['availableQuantity']
            ):
                return jsonify({'message': 'Name, Artist, Release Year, Music Style, Unitary Value and Available Quantity are required'}), 400
            
            if self.disc_service.get_disc_by_artist_and_name(request.json['artist'], request.json['discName']):
                return jsonify({'message': 'Disc already exists'}), 409

            disc = Disc(request.json['discName'], request.json['artist'], request.json['releaseYear'], request.json['musicStyle'], request.json['unitaryValue'], request.json['availableQuantity'])
            self.disc_service.create_disc(disc)
            return json.dumps(disc.__dict__), 201