from service.base import BaseService
from users.models import User
from database import async_session
from sqlalchemy import select, insert


class UserService(BaseService):
    model = User

