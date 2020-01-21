from json import JSONEncoder
from datetime import date


class DateEncoder(JSONEncoder):
    def default(self, obj):  # pylint: disable=E0202
        try:
            if isinstance(obj, date):
                return obj.isoformat()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)
