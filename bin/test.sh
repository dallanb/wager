#!/bin/sh

. ~/.bashrc
manage delete_db
manage flush_cache
manage init
pytest --disable-pytest-warnings -s
