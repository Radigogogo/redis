import pymssql
import redis
def setString(mkey,mval):
    pass

def tic_db_conn():

    # tic DB connection
    try:
        conn_ticdb = pymssql.connect(
            #server='PC-RADI_MA', #need to change to your db server
            server='127.0.0.1',
            user='Radi',
            password='phison',
            database='TIC_DB'
        )
        # #tic DB select
        # cursor = conn_ticdb.cursor(as_dict=True)
        # cursor.execute('select top 10 * from [TIC_DB].[dbo].[Card_Info]')
        #
        # print(cursor)
        # mkey = None
        # mval = None
        # for row in cursor:
        #     for key,value in row.items():
        #         #print(key+':'+str(value))
        #         print(key)


        #close tic db connection
        #conn_ticdb.close()

        return conn_ticdb
    except Exception as e:
        print(e)

def getDataFromSQLServer():
    conn_ticdb = tic_db_conn()
    #tic DB select
    cursor = conn_ticdb.cursor(as_dict=True)
    cursor.execute('select top 10 * from [TIC_DB].[dbo].[Card_Info]')
    mkey = None
    mval = None
    for row in cursor:
        #print('CardInfo_ID'+':'+str(row['CardInfo_ID']))
        #print(str(row.keys()))
        #mkey = 'CardInfo_ID'+':'+str(row['CardInfo_ID'])
        mval = ''

        for key,value in row.items():
            
            if str(key)== 'CardInfo_ID':
                mkey = str(key)+':'+str(value)
                # print(str(key)+':'+str(value))
            else:
                mval=






# def redis_conn():
#     try:
#         conn_redis_params = {
#             'host':  '127.0.0.1',
#             'port': 6379,
#             'db': 0
#         }
#         conn_redis = redis.StrictRedis(**conn_redis_params)
#         conn_redis.set('tt','123')
#         msg = conn_redis.get('tt')
#         print(msg)
#
#
#     except Exception as e:
#         print(e)






if __name__=='__main__':
    tic_db_conn()
    getDataFromSQLServer()
    #redis_conn()