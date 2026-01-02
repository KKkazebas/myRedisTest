import redis
import pytest

# 这是一个“固件”，每个测试函数开始前都会运行，用来连接Redis
@pytest.fixture
def redis_client():
    client = redis.Redis(host='localhost', port=6380, decode_responses=True)
    yield client  # 把连接对象传给测试函数
    client.flushdb()  # 测试结束后清空数据库，保证每个测试独立
    client.close()

# 测试用例1：能不能正常存一个字符串？
def test_set_get_string(redis_client):
    redis_client.set("name", "Alice")
    result = redis_client.get("name")
    assert result == "Alice"  # 断言：如果result等于"Alice"，测试通过

# 测试用例2：存一个数字，然后增加它
def test_incr(redis_client):
    redis_client.set("counter", 10)
    redis_client.incr("counter")
    result = redis_client.get("counter")
    assert result == "11"

# 测试用例3：设置一个过期时间，然后验证它过期
def test_expire(redis_client):
    redis_client.set("temp_key", "data", ex=1)  # ex=1 表示1秒后过期
    import time
    time.sleep(1.5)  # 等1.5秒
    result = redis_client.get("temp_key")
    assert result is None  # 断言：这个key应该已经不存在了