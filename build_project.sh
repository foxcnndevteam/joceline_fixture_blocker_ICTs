rm -rf dist
rm -rf build

pyinstaller JocelineFB.spec

cp -r static/lang/ dist/
cp -r static/jocelinefb.conf.json dist/
