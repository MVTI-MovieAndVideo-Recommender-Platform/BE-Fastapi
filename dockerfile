# 베이스 이미지 설정
FROM python:3.12.2-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 작업 디렉토리 설정
WORKDIR /app

COPY . /app

RUN pip3 install --no-cache-dir --upgrade -r /app/requirements.txt

# 컨테이너 포트 설정
EXPOSE 80

# FastAPI 애플리케이션 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]