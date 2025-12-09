#### 포트 공유 - 같은 와이파이
1. ipconfig -> ipv4 주소 찾기
2. django 설정 변경(settings.py)
```python
# settings.py
# 개발 중 편의를 위해 모든 호스트 허용 (배포 시에는 반드시 수정 필요)
ALLOWED_HOSTS = ['*'] 
# 또는 특정 IP만 허용
# ALLOWED_HOSTS = ['192.168.0.15', 'localhost', '127.0.0.1']
```
3. 서버 실행 커멘드 변경
> python manage.py runserver 0.0.0.0:8000
4. 동료 브라우저 주소 공유
> http://(ipv4주소/서버연사람거):8000
