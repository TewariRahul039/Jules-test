from flask import Blueprint, jsonify, request
from sqlalchemy import or_
from ..models.product import Product
from .. import db

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/products', methods=['GET'])
def get_products():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    pagination = Product.query.paginate(page=page, per_page=per_page, error_out=False)
    products = pagination.items

    return jsonify({
        'products': [product.to_dict() for product in products],
        'page': pagination.page,
        'per_page': pagination.per_page,
        'total_pages': pagination.pages,
        'total_products': pagination.total
    })

@api_bp.route('/products/search', methods=['GET'])
def search_products():
    query_param = request.args.get('query', '', type=str)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    if not query_param.strip():
        return jsonify({
            'products': [],
            'page': page,
            'per_page': per_page,
            'total_pages': 0,
            'total_products': 0,
            'message': 'Search query cannot be empty.'
        }), 400 # Optional: return 400 for empty query

    search_term = f'%{query_param}%'

    # Using ilike for case-insensitive search (SQLAlchemy handles this for SQLite vs PostgreSQL)
    base_query = Product.query.filter(
        or_(
            Product.name.ilike(search_term),
            Product.description.ilike(search_term)
        )
    )

    pagination = base_query.paginate(page=page, per_page=per_page, error_out=False)
    products = pagination.items

    return jsonify({
        'products': [product.to_dict() for product in products],
        'page': pagination.page,
        'per_page': pagination.per_page,
        'total_pages': pagination.pages,
        'total_products': pagination.total
    })

@api_bp.route('/products/filter', methods=['GET'])
def filter_products():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    category = request.args.get('category', type=str)
    min_price_str = request.args.get('min_price')
    max_price_str = request.args.get('max_price')

    query = Product.query

    if category:
        query = query.filter(Product.category.ilike(f'%{category}%')) # Using ilike for category too

    if min_price_str:
        try:
            min_price = float(min_price_str)
            query = query.filter(Product.price >= min_price)
        except ValueError:
            return jsonify({'error': 'Invalid min_price format.'}), 400

    if max_price_str:
        try:
            max_price = float(max_price_str)
            query = query.filter(Product.price <= max_price)
        except ValueError:
            return jsonify({'error': 'Invalid max_price format.'}), 400

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    products = pagination.items

    return jsonify({
        'products': [product.to_dict() for product in products],
        'page': pagination.page,
        'per_page': pagination.per_page,
        'total_pages': pagination.pages,
        'total_products': pagination.total
    })

@api_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product_by_id(product_id):
    product = db.session.get(Product, product_id) # Use db.session.get for primary key lookup
    if product:
        return jsonify(product.to_dict())
    else:
        return jsonify({'error': 'Product not found'}), 404

from ..services.chatbot_service import process_user_message

@api_bp.route('/chatbot', methods=['POST'])
def chat():
    data = request.get_json()
    if not data or 'message' not in data or not data['message'].strip():
        return jsonify({'error': 'Missing or empty message in request'}), 400

    user_message = data['message']
    response = process_user_message(user_message)
    return jsonify(response)
