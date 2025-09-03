from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "my-secret-key"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////Users/andorial/flask-watchlist/instance/watchlist.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    login_manager.init_app(app)

    from models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        db.create_all()
    
    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from watchlist_routes import watchlist as watchlist_blueprint
    app.register_blueprint(watchlist_blueprint)


    @app.route("/")
    def index():
        return render_template("index.html")
    
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)