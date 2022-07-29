import datetime
import calendar

import jwt
from flask import current_app, abort

from project.services.user import UserService


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def generate_tokens(self, email, password, is_refresh=False):
        """generate access_token and refresh_token"""
        user = self.user_service.get_by_email(email)

        if not is_refresh:
            if not self.user_service.compare_passwords(user.password, password):
               abort(401)

        data = {
            'email': user.email
        }

        # access_token
        min_add = datetime.datetime.utcnow() + datetime.timedelta(minutes=current_app.config.get('TOKEN_EXPIRE_MINUTES'))
        data['exp'] = calendar.timegm(min_add.timetuple())
        access_token = jwt.encode(data, current_app.config.get('JWT_SECRET'), algorithm=current_app.config.get('JWT_ALGORITHM'))

        # refresh_token
        days_add = datetime.datetime.utcnow() + datetime.timedelta(days=current_app.config.get('TOKEN_EXPIRE_DAYS'))
        data['exp'] = calendar.timegm(days_add.timetuple())
        refresh_token = jwt.encode(data, current_app.config.get('JWT_SECRET'), algorithm=current_app.config.get('JWT_ALGORITHM'))

        return {
            'access_token': access_token,
            'refresh_token': refresh_token
        }

    def get_email(self, refresh_token):
        """get email by refresh token"""
        data = jwt.decode(refresh_token,
                            current_app.config.get('JWT_SECRET'),
                            algorithms=[current_app.config.get('JWT_ALGORITHM')])
        return data.get('email')

    def approve_token(self, refresh_token):
        """approve token"""
        email = self.get_email(refresh_token)
        
        return self.generate_tokens(email, None, is_refresh=True)


