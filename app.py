import cherrypy
import os
import json
import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column , asc
from sqlalchemy.types import String, Integer ,DateTime
from cp_sqlalchemy import SQLAlchemyTool, SQLAlchemyPlugin
from jinja2 import Environment, FileSystemLoader

Base = declarative_base()
HERE = os.path.dirname(os.path.abspath(__file__))
env = Environment(loader=FileSystemLoader('templates'))

class Notes(Base):

    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True)
    title = Column(String(32))
    note = Column(String(32))
    created_date = Column(DateTime, default=datetime.datetime.utcnow)


class Notes_Class(object):

    @property
    def db(self):
        return cherrypy.request.db

    @cherrypy.expose
    def index(self):
        all_notes = self.db.query(Notes).order_by(asc(Notes.created_date))
        tmpl = env.get_template('notes.html')
        return tmpl.render(notes=all_notes)

    @cherrypy.expose
    def submit(self,title,note):
        self.db.add(Notes(title=title,note=note))
        self.db.commit()
        cherrypy.response.headers['Content-Type'] = 'application/json'
        return json.dumps(dict(title="%s " % title , note="%s " % note))

    @cherrypy.expose
    def update_data(self,note_id,title,note):
        self.db.query(Notes).filter(Notes.id == note_id).update({Notes.title: title ,Notes.note:note});
        self.db.commit();
        cherrypy.response.headers['Content-Type'] = 'application/json'
        return json.dumps(dict(title="%s " % title , note="%s " % note))

    @cherrypy.expose
    def delete_data(self,note_id):
        self.db.query(Notes).filter(Notes.id == note_id).delete();
        self.db.commit();
        cherrypy.response.headers['Content-Type'] = 'application/json'
        return json.dumps({'status':200})

class ListNotes_Class(object):

    @property
    def db(self):
        return cherrypy.request.db

    @cherrypy.expose
    def index(self):
       
        tmpl = env.get_template('listNotes.html')
        return tmpl.render()

   

def run():
    cherrypy.tools.db = SQLAlchemyTool()

    global_conf = {
        'global': {
            'server.socket_host': '127.0.0.1',
            'server.socket_port': int(os.environ.get('PORT', 5000)),
        },
        'databases':{
            'driver': "postgres",
            'host': "localhost",
            'port': 5432,
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
    cherrypy.tree.mount(Notes_Class(), '/', config=app_config)
    cherrypy.tree.mount(ListNotes_Class(), '/listNotes/', config=app_config)
    # dbfile = os.path.join(HERE, 'database1.db')

    # if not os.path.exists(dbfile):
    #     open(dbfile, 'w+').close()

    sqlalchemy_plugin = SQLAlchemyPlugin(
         cherrypy.engine, Base, 'postgresql+psycopg2://postgres:rootpass@0.0.0.0:5432/db3'
    )
    sqlalchemy_plugin.subscribe()
    sqlalchemy_plugin.create()
    
    cherrypy.engine.start()
    cherrypy.engine.block()


if __name__ == '__main__':
    run()



