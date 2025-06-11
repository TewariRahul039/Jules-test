import os
import click
from flask import Flask
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy extension
db = SQLAlchemy()

def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)

    # Load configuration from project.config module
    # Ensure this path is correct and config.py exists
    app.config.from_object('project.config.Config') # Using the base Config for now

    # Ensure the instance folder exists
    # Flask automatically creates this for instance_relative_config=True
    # when app.instance_path is accessed, but explicit creation is fine.
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        # Handle error if instance path cannot be created, though unlikely
        pass

    # Initialize Flask extensions
    db.init_app(app)

    # Import models here to ensure they are registered with SQLAlchemy
    # before creating tables.
    # Adjusted import path assuming models are in .models.product
    from .models.product import Product

    # Define and register the init-db command
    @click.command('init-db')
    @with_appcontext
    def init_db_command():
        """Clear existing data and create new tables."""
        # Import all models here before calling db.create_all()
        # This ensures all tables are known to SQLAlchemy
        db.create_all()
        click.echo('Initialized the database.')

    app.cli.add_command(init_db_command)

    # Import the data generator function
    from .utils.data_generator import generate_mock_products

    # Define and register the populate-db command
    @click.command('populate-db')
    @with_appcontext
    def populate_db_command():
        """Populate the database with mock products."""
        # Optionally, clear existing products first if desired
        # from .models.product import Product # Import here if you need to delete
        # Product.query.delete()
        # db.session.commit()
        # click.echo('Cleared existing products.')

        generate_mock_products(100) # Generate 100 products
        # The generate_mock_products function already prints a message.
        # click.echo('Populated the database with mock products.') # This might be redundant

    app.cli.add_command(populate_db_command)

    # Register API blueprint
    from .routes.api import api_bp
    app.register_blueprint(api_bp) # url_prefix is already defined in api_bp

    # Register Auth blueprint
    from .routes.auth import auth_bp
    app.register_blueprint(auth_bp) # url_prefix is defined in auth_bp

    return app
