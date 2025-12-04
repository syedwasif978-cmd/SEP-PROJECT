from models.vendor import Vendor
def list_vendors():
    return Vendor.query.all()
