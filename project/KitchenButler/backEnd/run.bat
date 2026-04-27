@echo off
chcp 65001
if not exist venv(
    echo 创建虚拟环境
    python -m venv venv
    echo 设置pip镜像
    pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
    pip config set install.trusted-host mirrors.aliyun.com
    call venv\Scripts\activate
    echo 下载环境，请稍等……
    pip install -r requirements.txt
)

call venv\Scripts\activate
python main