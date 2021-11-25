import datetime
from encoders import DateEncoder


def test_encoder():
    de = DateEncoder()
    assert type(de.default(datetime.datetime.now())) == str
    assert type(de.default(datetime.date.today())) == str
