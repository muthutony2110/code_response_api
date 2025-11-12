
import redis
import json

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def save_history(user_id, prompt, response):
    key = f"chat:{user_id}"
    entry = {"prompt": prompt, "response": response}
    r.rpush(key, json.dumps(entry))

def get_history(user_id, limit=3):
    key = f"chat:{user_id}"
    history_json = r.lrange(key, -limit, -1)
    return [json.loads(item) for item in history_json]

def clear_history(user_id):
    return r.delete(f"chat:{user_id}")

def get_all_history(user_id):
    key = f"chat:{user_id}"
    history_json = r.lrange(key, 0, -1)
    return [json.loads(item) for item in history_json]