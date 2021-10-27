import pymssql
import redis

# tic DB connection
conn_ticdb = pymssql.connect(
    server='PC-RADI_MA',
    user='Radi',
    password='phison',
    database='TIC_DB'
)

conn_redis_params = {
    'host' : '127.0.0.1',
    'port' : 6379,
    'db' : 0
}
conn_redis = redis.StrictRedis(**conn_redis_params )

#tic DB select
cursor = conn_ticdb.cursor(as_dict=True)
cursor.execute('select top 10 * from [TIC_DB].[dbo].[Card_Info]')
print(cursor)
for row in cursor :
    print(row)

#close tic db connection
conn_ticdb.close()