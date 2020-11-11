import logging

from src import db, WagerStatus


def init_wager_status(status_enums):
    logging.info(f"init_wager_status started")

    for status_enum in status_enums:
        status = WagerStatus(name=status_enum)
        db.session.add(status)
    db.session.commit()
    logging.info(f"init_wager_status completed")
    return
