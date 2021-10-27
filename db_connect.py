import pymssql
conn = pymssql.connect(
    server='PC-RADI_MA',
    user='Radi',
    password='phison',
    database='TIC_DB'
)

cursor = conn.cursor(as_dict=True)
cursor.execute('select top 10 * from [TIC_DB].[dbo].[Card_Info]')
# for row in cursor:
#     print(row[])
print(cursor)
for row in cursor :
    print(row)

# field_name=[i[0] for i in cursor.description]
# result=cursor.fetchall()
# for row in result :
#     print(row)


conn.close()