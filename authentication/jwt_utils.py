#auth_service > authentication > jwt_utils.py
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from jwt import ExpiredSignatureError, InvalidTokenError

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = 'HS256'
ACCESS_TOKEN_LIFETIME = timedelta(minutes=60) #토큰 만료시간 조절
REFRESH_TOKEN_LIFETIME = timedelta(days=7)

def create_access_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + ACCESS_TOKEN_LIFETIME,
        'type': 'access'
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + REFRESH_TOKEN_LIFETIME,
        'type': 'refresh'
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token, token_type='access'):
    print("🔍 auth-service가 받은 토큰:", token)  # 디버깅 로그

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("✅ 디코딩된 payload:", payload)  # 디버깅 로그

        if payload.get('type') != token_type:
            print("❌ 토큰 타입이 일치하지 않음:", payload.get('type'))  # 디버깅 로그
            raise InvalidTokenError('Invalid token type')

        return payload['user_id']
    except ExpiredSignatureError:
        print("❌ 토큰 만료됨")  # 디버깅 로그
        raise ExpiredSignatureError('Token expired')
    except InvalidTokenError as e:
        print("❌ 토큰 검증 실패:", str(e))  # 디버깅 로그
        raise InvalidTokenError('Invalid token')
    except Exception as e:
        print("❌ 알 수 없는 에러:", str(e))  # 추가 보호
        raise InvalidTokenError('Unknown error in token verification')