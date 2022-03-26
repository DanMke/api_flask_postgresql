from flask import jsonify, request, json
from model.disc import Disc
from service.disc_service import DiscService
import sys

class DiscController:
    def __init__(self, app, database):
        self.app = app
        self.disc_service = DiscService(database)
        self.routes()

    def routes(self):
        @self.app.route('/discs', methods=['GET'])
        def get_discs():
            args = request.args
            print(args, file=sys.stderr)
            print(args.to_dict(), file=sys.stderr)
            discs = self.disc_service.get_discs(args.to_dict())
            if discs is None:
                return [], 200
            return discs, 200

        @self.app.route('/discs/<disc_artist>/', methods=['GET'])
        def get_disc_by_artist(disc_artist):
            disc = self.disc_service.get_disc_by_artist(disc_artist)
            if disc is None:
                return jsonify({'message': 'Disc not found'}), 404
            return disc, 200

        @self.app.route('/discs/<disc_artist>/<discName>', methods=['GET'])
        def get_disc_by_artist_and_name(disc_artist, discName):
            disc = self.disc_service.get_disc_by_artist_and_name(disc_artist, discName)
            if disc is None:
                return jsonify({'message': 'Disc not found'}), 404
            return disc, 200

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
            disc_json = self.disc_service.create_disc(disc)
            return disc_json, 201

        @self.app.route('/discs/<disc_artist>/<discName>', methods=['PUT'])
        def decrement_disc_quantity(disc_artist, discName):
            disc = self.disc_service.update_disc_decrement_quantity(disc_artist, discName)
            if disc is None:
                return jsonify({'message': 'Disc not found'}), 404
            return disc, 200