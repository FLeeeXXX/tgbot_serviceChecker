from app.service.base import BaseService
from models import Site


class SiteService(BaseService):
    model = Site
