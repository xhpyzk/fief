# 设置环境变量
export DATABASE_LOCATION=./data/db
export SECRETS_DIR=./run/secrets

mkdir -p ./data/db
mkdir -p ./run/secrets

rm -rf dist
hatch build -t wheel
pip install dist/fief_server-0.28.6-py3-none-any.whl --force-reinstall

supervisord -c docker/supervisord.conf