from typing import List

from flask import current_app
from sqlalchemy import desc
from sqlalchemy.orm import scoped_session


class BaseDAO:
    def __init__(self, session: scoped_session, model):
        self.session = session
        self.model = model

    def get_one(self, pk):
        """get item by id"""
        return self.session.query(self.model).get(pk)

    def get_all(self, page = None, do_sort = False):
        """get all items"""
        content = self.session.query(self.model)

        if do_sort:
            content = content.order_by(desc(self.model.year))
        if page:
            content = content.limit(current_app.config.get('ITEMS_PER_PAGE')).offset((page-1) * current_app.config.get('ITEMS_PER_PAGE'))

        return content.all()
    
    def create(self, data):
        """create item"""
        item = self.model(**data)
        self.session.add(item)
        self.session.commit()
        return item

    def delete(self, pk):
        item = self.get_one(pk)
        self.session.delete(item)
        self.session.commit()