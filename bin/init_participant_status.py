import logging

from src import db, ParticipantStatus


def init_participant_status(status_enums):
    logging.info(f"init_participant_status started")

    for status_enum in status_enums:
        status = ParticipantStatus(name=status_enum)
        db.session.add(status)
    db.session.commit()
    logging.info(f"init_participant_status completed")
    return
