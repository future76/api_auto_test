# 关闭执行脚本输出
@echo off
# 延迟赋值
setlocal enabledelayedexpansion
set port=9999
set pid=bug
for /f "tokens=5" %%a in ('netstat -ano^|findstr %port%') do (
        set pid=%%a
)
if not "%pid%" == "bug" (
 taskkill /f /pid !pid!
 echo 服务已关闭
) else (
echo 服务未启动
)