"""
Tutorial - Hello World.

The most basic (working) CherryPy application possible.
"""
import json
import os.path

# Import CherryPy global namespace
import cherrypy
import ai

class HelloWorld:
    """Sample request handler class."""

    # Expose the index method through the web. CherryPy will never
    # publish methods that don't have the exposed attribute set to True.
    @cherrypy.expose
    def index(self):
        """Produce HTTP response body of hello world app index URI."""
        # CherryPy will call this method for the root URI ("/") and send
        # its return value to the client. Because this is tutorial
        # lesson number 01, we'll just send something really simple.
        # How about...
        return "Welcome!"

    @cherrypy.expose
    def get_rec(self, song_name):
        return json.dumps(ai.recommendations(song_name))




if __name__ == '__main__':
    # CherryPy always starts with app.root when trying to map request URIs
    # to objects, so we need to mount a request handler root. A request
    # to '/' will be mapped to HelloWorld().index().
    current_dir = os.path.dirname(os.path.abspath(__file__))
    web_dir = os.path.join(current_dir, 'web')
    config = {
        'global': {
            'server.socket_host': '127.0.0.1',  # Only accessible on your computer
            'server.socket_port': 8080,  # The address is http://127.0.0.1:8080
            'log.screen': True,  # Show messages in your terminal
        },
        '/': {  # Rules for the main part of your website
            'tools.staticdir.on': True,  # Turn on serving files directly
            'tools.staticdir.dir': web_dir,  # Look in the 'web' folder for files
            'tools.staticdir.index': 'index.html',  # Show index.html when you go to '/'
        },
        # No extra config needed for /get_my_message as it's a simple GET request
    }

    cherrypy.quickstart(HelloWorld(), '/', config=config)