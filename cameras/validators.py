from schematics import types
from schematics.models import Model


class CameraValidator(Model):
    T = types.DateTimeType(required=True)
    name = types.StringType(required=True)
    link = types.URLType(required=True)
    price = types.NumberType(required=True, min_value=1)
    spider = types.StringType(required=True, min_length=1)
    uid = types.StringType()
    ean = types.StringType()
    mfr = types.StringType()
