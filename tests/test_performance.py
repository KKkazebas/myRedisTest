import pytest
import os
from utils.benchmarker import RedisBenchmarker

def test_redis_set_stress():
    # 1. 实例化压测工具
    host = os.getenv("REDIS_HOST", "localhost")
    port = int(os.getenv("REDIS_PORT", "6379"))
    bm = RedisBenchmarker(host=host, port=port)
    
    # 2. 执行压测：10个线程，总共5000次SET操作
    print("\n开始执行压力测试...")
    metrics = bm.run_benchmark(total_requests=5000, concurrent_threads=10)
    
    # 3. 打印结果
    print(f"\n压测结果统计：")
    print(f"吞吐量 (TPS): {metrics['tps']}")
    print(f"错误率: {metrics['error_rate']}")
    print(f"平均耗时: {metrics['avg_latency_ms']} ms")

    # 4. 设置基准阈值断言
    assert metrics['tps'] > 2000, f"性能未达标，当前 TPS: {metrics['tps']}"
    assert metrics['error_rate'] == "0.0%", "压测过程中出现错误"