# 设置环境变量
export DATABASE_LOCATION=./data/db
export SECRETS_DIR=./run/secrets

# 获取操作系统名称
OS=$(uname)

mkdir -p ./data/db
mkdir -p ./run/secrets

rm -rf dist
hatch build -t wheel
pip install dist/fief_server-0.28.6-py3-none-any.whl --force-reinstall

# 判断操作系统并执行相应的复制操作
if [ "$OS" == "Darwin" ]; then
    echo "检测到 macOS 环境"
    cp .env.dev .env
elif [ "$OS" == "Linux" ]; then
    echo "检测到 Linux 环境"
    cp .env.prod .env
else
    echo "未知的操作系统: $OS"
    exit 1
fi

supervisord -c docker/supervisord.conf