# Python 베이스 이미지를 사용합니다.
FROM python:3.9-slim

# 작업 디렉토리를 설정합니다.
WORKDIR /app

# 현재 디렉토리의 내용을 컨테이너의 작업 디렉토리로 복사합니다.
COPY . /app

# 필요한 패키지를 설치합니다.
RUN pip install --no-cache-dir -r requirements.txt

# 환경 변수를 설정합니다.
# sports 디렉토리 내의 __init__.py 파일을 사용하여 Flask 애플리케이션을 실행합니다.
ENV FLASK_APP=shop
ENV FLASK_RUN_HOST=0.0.0.0

# 컨테이너가 시작될 때 실행될 명령어를 설정합니다.
CMD ["flask", "run"]

# 컨테이너의 5000번 포트를 노출합니다.
EXPOSE 5000
