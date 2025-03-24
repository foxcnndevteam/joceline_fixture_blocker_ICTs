Remove-Item -r .\dist

pyinstaller .\JocelineFB.spec

Copy-Item -r .\static\lang\ .\dist\
Copy-Item -r .\static\jocelinefb.conf.json .\dist\