#!/usr/bin/env python3
""" Auth module for the API """
from flask import request
from typing import List, TypeVar


class Auth:
    """ Auth class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        method checks if a path is excluded
        """
        if path is None or excluded_paths is None or excluded_paths == []:
            return True
        if path[-1] != '/':
            path += '/'
        if path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """ authorization_header method that returns None
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ current_user method that returns None
        """
        return None
