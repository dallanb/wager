from flask import g
import logging


def init_wager_status(status_enums):
    WagerStatus = g.src.WagerStatus

    for status_enum in status_enums:
        status = WagerStatus(name=status_enum)
        g.src.db.session.add(status)
        logging.info(f"{status_enum} added")
    g.src.db.session.commit()
    return
