from schematics import types
from schematics.models import Model


class CameraValidator(Model):
    T = types.DateTimeType(required=True)
    name = types.StringType(required=True)
    link = types.URLType(required=True)
    price = types.FloatType(required=True)
    spider = types.StringType(required=True)
    uid = types.StringType()
    ean = types.StringType()
    mfr = types.StringType()
