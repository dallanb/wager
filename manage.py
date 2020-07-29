from flask import g
from flask.cli import FlaskGroup
from src import app, db, common
from bin import init_wager_course, init_wager_status
import src

cli = FlaskGroup(app)


def full_init():
    create_db()
    initialize_statuses()
    initialize_courses()


def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


def initialize_statuses():
    with app.app_context():
        g.src = src
        init_wager_status(status_enums=common.WagerStatusEnum)
        return


def initialize_courses():
    with app.app_context():
        g.src = src
        init_wager_course()
        return


@cli.command("init")
def init():
    full_init()


@cli.command("reset_db")
def reset_db():
    create_db()


@cli.command("init_status")
def init_status():
    initialize_statuses()


@cli.command("init_course")
def init_course():
    initialize_courses()


if __name__ == "__main__":
    cli()
