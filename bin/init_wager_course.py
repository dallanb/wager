import logging
from flask import g
from csv import reader


def init_wager_course():
    Course = g.src.Course

    f = reader(open("statics/csv/golf.csv"))

    for golf_canada_row in f:
        golf_canada_id = golf_canada_row[0]
        course = Course(golf_canada_id=golf_canada_id)
        g.src.db.session.add(course)
        logging.info(f"{golf_canada_id} added")
    g.src.db.session.commit()
    return
