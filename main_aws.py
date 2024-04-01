from myapplication.app import app_instance
from mangum import Mangum

handler = Mangum(app_instance)