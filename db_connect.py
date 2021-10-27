import pymssql
import redis

def tic_db_conn():
    # tic DB connection
    try:
        conn_ticdb = pymssql.connect(
            server='PC-RADI_MA',
            user='Radi',
            password='phison',
            database='TIC_DB'
        )
        #tic DB select
        cursor = conn_ticdb.cursor(as_dict=True)
        cursor.execute('select top 10 * from [TIC_DB].[dbo].[Card_Info]')
        print(cursor)
        for row in cursor :
            print(row)
        #close tic db connection
        conn_ticdb.close()
    except Exception as e:
        print(e)

def redis_conn():
    try:
        conn_redis_params = {
            'host':  '127.0.0.1',
            'port': 6379,
            'db': 0
        }
        conn_redis = redis.StrictRedis(**conn_redis_params)
        conn_redis.set('tt','123')
        msg = conn_redis.get('tt')
        print(msg)

    except Exception as e:
        print(e)

if __name__=='__main__':
    tic_db_conn()
    redis_conn()