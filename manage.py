from flask import g
from flask.cli import FlaskGroup
from src import app, db
from bin import init_wager_status
import src

cli = FlaskGroup(app)

@cli.command("full_init")
def full_init():
    create_db()
    initialize_statuses()

@cli.command("reset_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("drop_db")
def drop_db():
    db.drop_all()

@cli.command("init_wager_status")
def initialize_statuses():
    with app.app_context():
        g.src = src
        init_wager_status()
        return


if __name__ == "__main__":
    cli()
