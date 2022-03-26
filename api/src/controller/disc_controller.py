from flask import jsonify, request, json
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
            discs = self.disc_service.get_discs()
            if discs is None:
                return [], 200
            return discs, 200

        @self.app.route('/discs/<disc_artist>/<disc_name>', methods=['GET'])
        def get_disc_by_artist_and_name(disc_artist, disc_name):
            disc = self.disc_service.get_disc_by_artist_and_name(disc_artist, disc_name)
            if disc is None:
                return jsonify({'message': 'Disc not found'}), 404
            return disc, 200

        @self.app.route('/discs', methods=['POST'])
        def create_disc():
            if not request.json:
                return jsonify({'message': 'No data provided'}), 400
            elif (
                'artist' not in request.json or 'disc_name' not in request.json or 
                'release_year' not in request.json or 'music_style' not in request.json or 
                'unitary_value' not in request.json or 'available_quantity' not in request.json or 
                not request.json['disc_name'] or not request.json['artist'] or 
                not request.json['release_year'] or not request.json['music_style'] or 
                not request.json['unitary_value']or not request.json['available_quantity']
            ):
                return jsonify({'message': 'Name, Artist, Release Year, Music Style, Unitary Value and Available Quantity are required'}), 400
            
            if self.disc_service.get_disc_by_artist_and_name(request.json['artist'], request.json['disc_name']):
                return jsonify({'message': 'Disc already exists'}), 409

            disc = Disc(request.json['disc_name'], request.json['artist'], request.json['release_year'], request.json['music_style'], request.json['unitary_value'], request.json['available_quantity'])
            disc_json = self.disc_service.create_disc(disc)
            return disc_json, 201

        @self.app.route('/discs/<disc_artist>/<disc_name>', methods=['PUT'])
        def decrement_disc_quantity(disc_artist, disc_name):
            disc = self.disc_service.update_disc_decrement_quantity(disc_artist, disc_name)
            if disc is None:
                return jsonify({'message': 'Disc not found'}), 404
            return disc, 200