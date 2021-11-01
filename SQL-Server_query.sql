declare @d datetime
set @d=getdate()
SELECT Running_StartTime, Test_End_Time,
(SELECT Name1 FROM dbo.VRs_View_Code_Describe WHERE System = 'VRS' AND Type = '101' AND Code = TK.Test_Result) AS Test_Result,
(SELECT Name1 FROM dbo.VRs_View_Code_Describe WHERE System = 'VRS' AND Type = '100' AND Code = TK.Test_Status) AS Test_Status,
TK.TL_ID,
Tool_Name,
Tool_Version,
PT.Test_Result AS Pattern_Result,
PT.Pattern_Name,
PT.Test_Duration AS Pattern_Duration,
TK.Tester_ID,
TK.Test_Status
FROM dbo.VRs_View_Base_Task AS TK
LEFT JOIN dbo.Tool_List TL ON TK.TL_ID = TL.TL_ID
LEFT JOIN dbo.Pattern_List PT ON TK.TK_ID = PT.TK_ID


select [語句執行花費時間(毫秒)]=datediff(ms,@d,getdate())