from google.appengine.ext.webapp.util import run_wsgi_app
from utils.webapp.wsgi import WSGIApplication
from utils.routes.mapper import Mapper
from utils.utils import browser_check
map = Mapper(explicit = True)
from urls import url_routes



def RequestHandler():
    """
    
    Initiates the WSGI Application
    urls.py contains url mappings

    """
    url_routes(map)
    app = WSGIApplication(map, debug = True) 
    app = browser_check(app)
    run_wsgi_app(app)
                                

if __name__ == "__main__":
  RequestHandler()







