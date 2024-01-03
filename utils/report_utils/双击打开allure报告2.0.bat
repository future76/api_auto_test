@echo off
if "%1" == "h" goto begin
mshta vbscript:createobject("wscript.shell").run("""%~nx0"" h",0)(window.close)&&exit
:begin
::启动一个web服务监听9999端口，在后台运行。默认用当前文件夹的index.html作为首页
start /b http_server.exe -port 9999
::使用默认浏览器打开web服务的地址并等待浏览器关闭
start "" /WAIT http://127.0.0.1:9999
