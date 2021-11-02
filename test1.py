import pymssql
import redis

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
        #tic DB select
        cursor = conn_ticdb.cursor(as_dict=True)
        #cursor.execute('select top 10 * from [TIC_DB].[dbo].[Card_Info]')
        query = """
                    
            with 
            tt as(
            SELECT TOP(10)
            TK.TL_ID,
            ISNULL(TK.Tester_ID, 0) as Tester_ID,
            TK.Test_Status,
            ISNULL(Running_StartTime,0) as Running_StartTime, 
            Test_End_Time,
            (SELECT Name1 FROM dbo.VRs_View_Code_Describe WHERE System = 'VRS' AND Type = '101' AND Code = TK.Test_Result) AS Test_Result,
            (SELECT Name1 FROM dbo.VRs_View_Code_Describe WHERE System = 'VRS' AND Type = '100' AND Code = TK.Test_Status) AS Test_Status_2,
            Tool_Name,
            Tool_Version,
            ISNULL(PT.Test_Result,0) AS Pattern_Result,
            ISNULL(PT.Pattern_Name, 0) as Pattern_Name,
            ISNULL(PT.Test_Duration,0) AS Pattern_Duration
            FROM dbo.VRs_View_Base_Task AS TK
            LEFT JOIN dbo.Tool_List TL ON TK.TL_ID = TL.TL_ID
            LEFT JOIN dbo.Pattern_List PT ON TK.TK_ID = PT.TK_ID
            )
            
            Select * 
            from  tt 
            for json auto
        """
        cursor.execute(query)
        #print(cursor)
        mkey = None
        mval = None
        for row in cursor:
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
    #redis_conn()