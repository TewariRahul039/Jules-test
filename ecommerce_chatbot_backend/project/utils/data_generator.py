from faker import Faker
from .. import db # Assuming db is initialized in project/__init__.py
from ..models.product import Product # Assuming Product model is in project/models/product.py

def generate_mock_products(num_products=100):
    """Generates mock products and adds them to the database."""
    faker = Faker()

    categories = ('Electronics', 'Books', 'Clothing', 'Home & Kitchen', 'Sports & Outdoors', 'Toys & Games', 'Beauty & Personal Care')

    products_added = 0
    for _ in range(num_products):
        # Ensure price is realistic, e.g., between 5.00 and 500.00
        price = round(faker.random_int(min=500, max=50000) / 100.0, 2)
        if price <= 0: # Basic sanity check for price
            price = round(faker.random_element(elements=(10.0, 20.0, 50.0, 100.0)),2)


        product = Product(
            name=faker.unique.company() + " " + faker.word(ext_word_list=['gadget', 'device', 'tool', 'accessory', 'item', 'ware']), # More varied names
            description=faker.text(max_nb_chars=200),
            price=price,
            category=faker.random_element(elements=categories),
            image_url=faker.image_url(width=400, height=300, placeholder_url='https://via.placeholder.com/400x300.png?text=No+Image'), # Added placeholder
            stock_quantity=faker.random_int(min=0, max=200) # Increased max stock
        )
        db.session.add(product)
        products_added +=1

    try:
        db.session.commit()
        print(f'{products_added} mock products added to the database.')
    except Exception as e:
        db.session.rollback()
        print(f"Error adding mock products: {e}")
        # Attempt to add products one by one if batch commit fails, for debugging
        # This is less efficient and generally not for production, but can help identify problematic data.
        # print("Attempting to add products individually...")
        # products_added_individually = 0
        # for i in range(num_products): # Re-generate or use a pre-generated list
        #     # Re-generate product instance or ensure it's not already session-bound from previous attempt
        #     # This part would need careful handling if re-using instances
        #     # For simplicity, this example assumes you might re-generate or have a list of transient objects
        #     try:
        #         # Simplified re-generation for example
        #         price_ind = round(faker.random_int(min=500, max=50000) / 100.0, 2)
        #         product_ind = Product(
        #             name=faker.unique.company() + " " + faker.word(),
        #             description=faker.text(max_nb_chars=200),
        #             price=price_ind if price_ind > 0 else 10.0,
        #             category=faker.random_element(elements=categories),
        #             image_url=faker.image_url(width=400, height=300, placeholder_url='https://via.placeholder.com/400x300.png?text=No+Image'),
        #             stock_quantity=faker.random_int(min=0, max=200)
        #         )
        #         db.session.add(product_ind)
        #         db.session.commit()
        #         products_added_individually += 1
        #     except Exception as individual_e:
        #         db.session.rollback()
        #         print(f"Failed to add product (name: {product_ind.name if 'product_ind' in locals() else 'N/A'}): {individual_e}")
        # if products_added_individually > 0:
        #    print(f"{products_added_individually} products added individually after initial batch failure.")

    # Clear Faker's unique provider state for 'company' if you plan to call this function multiple times
    # in the same Python process and expect fresh unique values across calls.
    # Faker.clear_instance_providers() # This clears all, be specific if needed or handle state externally.
    # For 'unique.company()', it's often simpler to reinstantiate Faker or manage the unique state if necessary.
    # For this script, if called multiple times via flask CLI, it's a new process each time, so less of a concern.

if __name__ == '__main__':
    # This part is for direct execution testing (optional)
    # You would need to set up a Flask app context manually to use db.session
    print("This script is intended to be called via Flask CLI (e.g., flask populate-db)")
    print("To test generate_mock_products directly, you need an active Flask app context.")
    # Example of manual context (requires app and db to be available):
    # from project import create_app, db
    # app = create_app()
    # with app.app_context():
    #     generate_mock_products(10)
    #     print(Product.query.count())
