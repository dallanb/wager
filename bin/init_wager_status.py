from flask import g
import logging


def init_wager_status(status_enums):
    logging.info(f"init_wager_status started")
    WagerStatus = g.src.WagerStatus

    for status_enum in status_enums:
        status = WagerStatus(name=status_enum)
        g.src.db.session.add(status)
    g.src.db.session.commit()
    logging.info(f"init_wager_status completed")
    return
