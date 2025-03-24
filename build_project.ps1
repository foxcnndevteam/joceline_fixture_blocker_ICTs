rm -r .\dist

pyinstaller .\JocelineFB.spec

cp -r .\static\lang\ .\dist\
cp -r .\static\jocelinefb.conf.json .\dist\