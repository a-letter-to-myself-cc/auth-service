# 베이스 이미지
FROM python:3.11-slim

# 작업 디렉토리 생성
WORKDIR /app

# 종속성 복사 및 설치
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# 환경변수들을 build 시점에 넘김
ARG DB_NAME
ARG DB_USER
ARG DB_PASSWORD
ARG DB_HOST

# 환경변수를 런타임에도 사용할 수 있게 설정
ENV DB_NAME=$DB_NAME \
    DB_USER=$DB_USER \
    DB_PASSWORD=$DB_PASSWORD \
    DB_HOST=$DB_HOST

# 프로젝트 코드 복사
COPY . /app

# 포트 설정
ENV PORT=8001
EXPOSE 8001

# entrypoint 추가
COPY entrypoint.sh /entrypoint.sh
RUN apt-get update && apt-get install -y netcat-openbsd
RUN chmod +x /entrypoint.sh

# 실행 커맨드 교체
CMD ["/entrypoint.sh"]

# 서버 실행
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
