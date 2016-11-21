#!/usr/bin/env bash
gunicorn --reload --max-requests 1 -b 0.0.0.0:$PORT app:app