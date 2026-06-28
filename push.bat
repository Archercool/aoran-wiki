@echo off
echo 正在同步知识库到GitHub...
git add .
for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do set datetime=%%I
set commitmsg="自动更新 %datetime:~0,4%-%datetime:~4,2%-%datetime:~6,2% %datetime:~8,2%:%datetime:~10,2%"
git commit -m %commitmsg%
git push
echo 同步完成！
pause