# OneScriptBuild NGROK
Simplify the building of ngrok with golang (you don't even to install golang environment)

## Usage
~~~
./python3 build_release.py

  -t --target DOMAIN             your domain
  -s --server                    build server
  -c --client                    build client
  -a --amd64                     build with GOARCH=amd64
  -i --i386                      build with GOARCH=386
  -l --linux                     build for Linux
  -w --windows                   build for windows
  -m --macos                     build for macos
  -h --help                      show help
~~~

## Caution
build_release.py can only be executed on Linux, be mind.
(this package contains golang environment and ngrok source codes)
