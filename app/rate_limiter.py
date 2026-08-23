from fastapi import Request,HTTPException
from app.redis import redis_client

LIMIT = 60
WINDOW = 100

def check_rate_limit(request:Request):
    client_ip = request.client.host
    key= f"rate_limit:{client_ip}"
    current_count = redis_client.incr(key)
    if current_count == 1:
        redis_client.expire(key,ex=WINDOW)
        return
    if int(current_count)>= LIMIT:
        raise HTTPException(status_code=429,detail="Too many Requests")
    