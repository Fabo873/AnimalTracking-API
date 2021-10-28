if [ -x "$(command -v docker)" ]; then
    echo "Docker -> OK"
    echo ''
else
    echo "Docker not installed"
    echo ''
    exit 1
fi

echo 'Docker Down'
echo ''
docker-compose down
echo ''

echo 'Delete Env'
echo ''
rm -r ./env
echo ''