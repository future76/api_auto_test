@echo off 
if "%1" == "h" goto begin 
mshta vbscript:createobject("wscript.shell").run("%~nx0 h",0)(window.close)&&exit 
:begin
cd ..
:: 【注意：这里的 report_allure 替换成你自己报告文件夹的名字】
allure open ./api-automation-testing/report/allure_report
