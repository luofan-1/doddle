@REM .doddleenv/Scripts/activate
set APP_NAME="doddle v1.0.0"
set DISTPATH="D:/projects/doddle/app/dist"
set WORKPATH="D:/projects/doddle/app/build"
set SPECPATH="D:/projects/doddle/app"
set DATAPATH="D:/projects/doddle/.doddleenv/Lib/site-packages/customtkinter;customtkinter"
pyinstaller -w -F --noconsole --clean --distpath %DISTPATH% --workpath %WORKPATH% --specpath %SPECPATH% --add-data %DATAPATH% --name %APP_NAME% main.py