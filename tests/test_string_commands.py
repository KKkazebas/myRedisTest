import redis
import pytest
import os
# 这是一个“固件”，每个测试函数开始前都会运行，用来连接Redis
@pytest.fixture
def redis_client():
    host = os.getenv("REDIS_HOST", "redis")
    port = int(os.getenv("REDIS_PORT", "6379"))
    #本地运行使用set "REDIS_HOST=localhost" && set "REDIS_PORT=6380" && pytest
    client = redis.Redis(host=host, port=port, decode_responses=True)
    client.flushdb() 
    yield client
    
    client.flushdb() 
    client.close()

# +set&get一个普通字符串
def test_set_normal(redis_client):
    redis_client.set("str", "adb2()*")
    result = redis_client.get("str")
    assert result == "adb2()*" 

# +set存一个空字符串
def test_set_null(redis_client):
    redis_client.set("str", "")
    result = redis_client.get("str")
    assert result == "" 

# -set缺少value参数
def test_set_without_value(redis_client):
    with pytest.raises(redis.exceptions.ResponseError) as exc_info:
        redis_client.execute_command('SET', 'mykey')
    error_msg = str(exc_info.value)
    assert "wrong number of arguments" in error_msg.lower()

# -set过期时间参数名不正确
def test_set_wrong_name_of_outdate(redis_client):
    with pytest.raises(redis.exceptions.ResponseError) as exc_info:
        redis_client.execute_command('SET', 'mykey','haha','time',10)#time->ex
    error_msg = str(exc_info.value)
    assert "syntax error" in error_msg.lower()

# -set过期时间参数值不正确 为非数字
def test_set_noNumValue_of_outdate(redis_client):
    with pytest.raises(redis.exceptions.ResponseError) as exc_info:
        redis_client.execute_command('SET', 'mykey','haha','ex','nonumber')
    error_msg = str(exc_info.value)
    assert "value is not an integer or out of range" in error_msg.lower()

# -set过期时间参数值不正确 为非正数
def test_set_noPositivenumValue_of_outdate(redis_client):
    with pytest.raises(redis.exceptions.ResponseError) as exc_info:
        redis_client.execute_command('SET', 'mykey','haha','ex',-10)
    error_msg = str(exc_info.value)
    assert "invalid expire time" in error_msg.lower()

# -set超出边界值 待实现
#def test_set_no_value(redis_client):
#    with pytest.raises(redis.exceptions.ResponseError) as exc_info:
#        redis_client.execute_command('SET', 'mykey','haha')
#    error_msg = str(exc_info.value)
#    assert "syntax error" in error_msg.lower()

# -get一个不存在的key
def test_get_noExistsKey(redis_client):
    result = redis_client.get("str")
    assert result == None

# -get缺少参数
def test_get_without_value(redis_client):
    with pytest.raises(redis.exceptions.ResponseError) as exc_info:
        redis_client.execute_command('GET')
    error_msg = str(exc_info.value)
    assert "wrong number of arguments" in error_msg.lower()