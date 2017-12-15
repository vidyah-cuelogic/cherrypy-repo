import cherrypy
import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy.types import String, Integer
from cp_sqlalchemy import SQLAlchemyTool, SQLAlchemyPlugin
from jinja2 import Environment, FileSystemLoader
import json
Base = declarative_base()
HERE = os.path.dirname(os.path.abspath(__file__))
env = Environment(loader=FileSystemLoader('templates'))

class Notes(Base):

    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True)
    note = Column(String(32))

class Root(object):

    @property
    def db(self):
        return cherrypy.request.db

    # @cherrypy.expose()
    # @cherrypy.tools.json_in()
    # @cherrypy.tools.json_out()
    # def UsernameExists(self):
    #     import pdb; pdb.set_trace();
    #     json_obj = cherrypy.request.json
    #     usernames = ['bruce', 'lee', 'jackie', 'chan']
    #     return {"exists": json_obj['username'] in usernames}

    @cherrypy.expose
    def submit(self, note):
        self.db.add(Notes(note=note))
        self.db.commit()
        for msg in self.db.query(Notes).all():
            print msg.note
            print "=================="
        cherrypy.response.headers['Content-Type'] = 'application/json'
        return json.dumps(dict(title="Hello, %s" % note))

    @cherrypy.expose
    def index(self, note=None):
        if note: 
            self.db.add(Notes(note=note))
            self.db.commit()
            raise cherrypy.HTTPRedirect('/')

        tmpl = env.get_template('index.html')
        return tmpl.render()



def run():
    cherrypy.tools.db = SQLAlchemyTool()

    global_conf = {
        'global': {
            'server.socket_host': '0.0.0.0',
            'server.socket_port': int(os.environ.get('PORT', 5000)),
        },
        'databases':{
            'driver': "sqlite"
        }
    }
    cherrypy.config.update(global_conf)

    app_config = {
        '/': {
            'tools.db.on': True,
        },
        '/static': {
            'tools.staticdir.root': os.path.dirname(os.path.abspath(__file__)),
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'static',
        },    
        
    }
    cherrypy.tree.mount(Root(), '/', config=app_config)
    dbfile = os.path.join(HERE, 'db3.db')

    if not os.path.exists(dbfile):
        open(dbfile, 'w+').close()

    sqlalchemy_plugin = SQLAlchemyPlugin(
         cherrypy.engine, Base, 'sqlite:///%s' % (dbfile),
        echo=True
    )
    sqlalchemy_plugin.subscribe()
    sqlalchemy_plugin.create()
    
    cherrypy.engine.start()
    cherrypy.engine.block()


if __name__ == '__main__':
    run()
