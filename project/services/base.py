from flask import abort


class BaseService:
    def __init__(self, dao):
        self.dao = dao

    def get_one(self, pk):
        item = self.dao.get_one(pk)
        if not item:
            abort(404)
        return item

    def get_all(self, page, do_sort=False):
        items = self.dao.get_all(page, do_sort)
        if not items:
            abort(404)
        return items
    
    def create(self, data):
        return self.dao.create(data)