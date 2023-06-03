# Dockerfile

FROM python:3.10-slim-buster

COPY . /app

WORKDIR /app

RUN pip install --upgrade setuptools -i https://pypi.tuna.tsinghua.edu.cn/simple \
&& pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple \
&& pip install -v -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

CMD ["python", "main.py"]