from flask import g
import logging


def init_participant_status(status_enums):
    logging.info(f"init_participant_status started")
    ParticipantStatus = g.src.ParticipantStatus

    for status_enum in status_enums:
        status = ParticipantStatus(name=status_enum)
        g.src.db.session.add(status)
    g.src.db.session.commit()
    logging.info(f"init_participant_status completed")
    return
