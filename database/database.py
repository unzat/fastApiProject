import fdb

def get_database_connection():
    return fdb.connect(
        dsn='localhost/3053:PATRIA_FB30_LOCAL',
        user='SYSDBA',
        password='masterkey',
        charset='UTF8'
    )

def get_database_connection_web():
    return fdb.connect(
        dsn='192.168.65.11/3050:PATRIA_WEB_FB30',
        user='SYSDBA',
        password='##.*infor',
        charset='UTF8'
    )
