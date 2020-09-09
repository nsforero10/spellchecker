from sqlalchemy import (create_engine, Table) 
from sqlalchemy.orm import scoped_session, sessionmaker

class DBStorage:

    _engine = None

    def __init__(self):
        '''instantiate  a DBStorage object'''
        USER = 'root'
        PWD = 'admin'
        HOST = 'localhost'
        DB = 'treble_test'
        self._engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(USER, PWD, HOST, DB))

    def save_history(self, request=None, result=None):
        '''saves the history'''
        if request is not None and result is not None:
            with self._engine.connect() as connection:
                response = connection.execute('insert into spell_check_history (request, result) values ("{}", "{}")'.format(request, result))
                print(response)
