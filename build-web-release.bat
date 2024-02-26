@echo off
REM make sure we are in the right directory
cd %~dp0
echo deleting build files in 3 seconds
timeout /t 3 /nobreak

REM remove the old build, dist and JackGamesMulticart folders if they are still around
rmdir /s /q dist
rmdir /s /q build
rmdir /s /q JackGamesMulticart
del *.spec
del *.zip


echo starting new web build in 3 seconds
timeout /t 3 /nobreak

cd ..
pygbag --build multicart

echo ------------------------------------------------------
echo build complete, making zip file
echo ------------------------------------------------------
timeout /t 3 /nobreak
cd multicart/build
7z a -tzip web.zip web

echo ------------------------------------------------------
echo zip file complete, moving to project root
echo ------------------------------------------------------
timeout /t 3 /nobreak
move web.zip ..
cd ..

echo ------------------------------------------------------
echo moving zip file complete, cleaning up garbage
echo ------------------------------------------------------
timeout /t 3 /nobreak
rmdir /s /q dist
rmdir /s /q build
rmdir /s /q JackGamesMulticart
del *.spec