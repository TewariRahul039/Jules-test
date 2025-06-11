from project import create_app

# Create the Flask app instance
app = create_app()

@app.route('/')
def hello():
    return "Backend is running!"

if __name__ == '__main__':
    # Note: app.run() is suitable for development.
    # For production, use a WSGI server like Gunicorn or uWSGI.
    app.run(debug=True)
