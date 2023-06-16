from app import app
from data import data
from render import render

if __name__ == "__main__":

    app.register_blueprint(data)
    app.register_blueprint(render)

    app.run(host="0.0.0.0", port=5000, debug=True)