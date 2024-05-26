#!/usr/bin/env python3
""" Module of Session Exp Auth """
from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """ Session Exp Auth class
    """
    session_duration = 0

    def __init__(self):
        """ Constructor
        """
        try:
            self.session_duration = int(getenv('SESSION_DURATION'))
        except Exception:
            pass

    def create_session(self, user_id: str = None) -> str:
        """ Creates a Session ID for a user_id
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Returns a User ID based on a Session ID
        """
        if session_id is None:
            return None
        session_dict = self.user_id_by_session_id.get(session_id)
        if session_dict is None:
            return None
        if self.session_duration <= 0:
            return session_dict.get('user_id')
        if 'created_at' not in session_dict:
            return None
        created_at = session_dict.get('created_at')
        window = created_at + timedelta(seconds=self.session_duration)
        if window < datetime.now():
            return None
        return session_dict.get('user_id')
