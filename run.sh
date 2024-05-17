# 设置环境变量
export DATABASE_LOCATION=./data/db
export SECRETS_DIR=./run/secrets

mkdir -p ./data/db
mkdir -p ./run/secrets

supervisord -c docker/supervisord.conf