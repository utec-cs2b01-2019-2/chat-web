from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import DeclarativeMeta
import json

class Manager:
    Base = declarative_base()
    session = None

    def createEngine(self):
        engine = create_engine('postgres://hribcqprejxxei:b42fa09eb13c51505c26bc43771c8f4077209df3b75388dcf59aba63141014e8@ec2-23-21-129-125.compute-1.amazonaws.com:5432/dfm5tb1l84iknu', echo=False)
        self.Base.metadata.create_all(engine)
        return engine

    def getSession(self, engine):
        if self.session == None:
            Session = sessionmaker(bind=engine)
            session = Session()

        return session

class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data)
                    fields[field] = data
                except TypeError:
                    fields[field] = None

            return fields

        return json.JSONEncoder.default(self, obj)
