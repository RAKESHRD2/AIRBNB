from flask import Flask, request, jsonify
from utils.data_handler import read_data, write_data

app = Flask(__name__)

# Loading the data
listings_data = read_data("data/airbnb.json")

# GET ENDPOINT
@app.route('/listings', methods=['GET'])
def get_all_listings():
    return jsonify(listings_data)

#BASED ON ID
@app.route('/listings/<int:listing_id>', methods=['GET'])
def get_listing_by_id(listing_id):
    listing = next((item for item in listings_data if item['id'] == listing_id), None)
    if listing:
        return jsonify(listing)
    return jsonify({'error': 'Listing not found'}), 404

#BASED ON QUARY
@app.route('/listings/search', methods=['GET'])
def get_listings_by_parameters():
    # Example: /listings/search?neighborhood=Downtown&room_type=Entire%20home%2Fapt
    filters = request.args
    filtered_listings = [listing for listing in listings_data if all(listing.get(key) == value for key, value in filters.items())]
    return jsonify(filtered_listings)

#POST ENDPOINT
@app.route('/listings', methods=['POST'])
def create_listing():
    new_listing = request.json
    if all(key in new_listing for key in ('name', 'price', 'neighborhood', 'host_id', 'room_type')):
        new_listing['id'] = len(listings_data) + 1
        listings_data.append(new_listing)
        return jsonify(new_listing), 201
    return jsonify({'error': 'Missing required fields'}), 400


@app.route('/listings/search', methods=['POST'])
def search_listings():
    search_terms = request.json.get('search_terms', [])
    if not search_terms:
        return jsonify({'error': 'No search terms provided'}), 400

    matching_listings = []
    for term in search_terms:
        matching_listings.extend([listing for listing in listings_data if term.lower() in listing['name'].lower()])

    return jsonify(matching_listings)

#PATCH ENDPOINT
@app.route('/listing/<int:listing_id>', methods=['PATCH'])
def update_listing(listing_id):
    listing = next((item for item in listings_data if item['id'] == listing_id), None)
    if listing:
        update_data = request.json
        listing.update(update_data)
        return jsonify(listing)
    return jsonify({'error': 'Listing not found'}), 404

#DELETE ENDPOINT
@app.route('/listing/<int:listing_id>', methods=['DELETE'])
def delete_listing(listing_id):
    global listings_data
    initial_length = len(listings_data)
    listings_data = [listing for listing in listings_data if listing['id'] != listing_id]
    
    if len(listings_data) < initial_length:
        return jsonify({'message': 'Listing deleted successfully'})
    
    return jsonify({'error': 'Listing not found'}), 404


if __name__ == '__main__':
    app.run(debug=True)
