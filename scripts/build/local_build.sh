#!/bin/sh

if [ -x "$(command -v python3)" ]; then
    echo "Python3 -> OK"
    echo ''
else
    echo "Python3 not installed"
    echo ''
    exit 1
fi

if python ./scripts/build/version.py; then
  echo 'Python3 version -> OK'
  echo ''
else
  echo 'Wrong Python version'
  echo ''
  exit 1
fi

if [ -x "$(command -v pip3)" ]; then
    echo "Pi3 -> OK"
    echo ''
else
    echo "Pi3 not installed"
    echo ''
    exit 1
fi

if [ -x "$(command -v docker)" ]; then
    echo "Docker -> OK"
    echo ''
else
    echo "Docker not installed"
    echo ''
    exit 1
fi



echo 'Instaling virtualenv'
pip3 install virtualenv
echo ''

if [ ! -d "./env" ]; then
  # Control will enter here if $DIRECTORY doesn't exist.
  echo 'Creating virtual env'
  echo ''
  virtualenv env
  echo ''
fi


case "$(uname -s)" in

   Darwin)
     echo 'Mac OS X'
     echo ''
     source env/bin/activate
     echo ''
     ;;

   Linux)
     echo 'Linux'
     echo ''
     source env/bin/activate
     echo ''
     ;;

   CYGWIN*|MINGW32*|MSYS*|MINGW*)
     echo 'MS Windows'
     echo ''
     source env/Scripts/activate
     echo ''
     ;;

   # Add here more strings to compare
   # See correspondence table at the bottom of this answer

   *)
     echo 'Only supported Linux, Mac OS, and Windows'
     echo ''
     exit 1 
     ;;
esac

echo 'Installing requirements'
echo ''
pip3 install -r requirements.txt
echo ''

echo 'Docker Up'
echo ''
docker-compose up -d
echo ''

echo 'Run API'
echo ''
python ./src/app.py
echo ''
