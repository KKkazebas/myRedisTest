
# Redis 自动化测试实践

## 注意 该项目处于非常早期

> 一个面向 Redis 的自动化测试练习项目：用 **Pytest** 设计核心命令的单元/集成测试，用 **Docker Desktop** 快速拉起测试环境，并为后续接入 **GitHub Actions** 做准备。  
> 当前进度：已完成部分 **基础命令** 的功能测试设计与实现（持续迭代中）。

---

## 项目亮点

- 基于 **Pytest + Docker +（规划）GitHub Actions** 构建 Redis 自动化测试平台，覆盖功能、性能、异常场景验证
- 使用 **等价类** 与 **边界值** 方法设计 Redis 核心命令测试用例（SET/GET/INCR/EXPIRE），并实现 **参数化测试**
- 规划开发 **多线程并发压测模块**，对 SET 操作进行压测，量化 QPS 并建立性能基准
- 规划集成 **GitHub Actions CI/CD**，实现提交自动触发测试并生成可视化报告

---

## 技术栈

- **Python**
- **Pytest**
- **Redis**
- **Docker Desktop**
- **GitHub Actions**
- **pytest-html**

---

## 目录结构

```text

```

---

## 快速开始



---

## 已实现测试范围

- 基础功能验证（持续扩展中）
  - `SET / GET`：正常写入读取、覆盖写、空值/特殊字符以及参数错误等场景

---

## 测试设计方法

- **等价类划分**
  - 合法输入：正常 key/value、不同长度、不同字符集
- **边界值分析**

---

## 规划路线图

- [ ] 覆盖更多命令与数据结构：Hash / List / Set / ZSet
- [ ] 增加异常/容错场景：连接中断、超时、网络抖动模拟（在 Docker 环境中注入）
- [ ] 性能与并发模块：多线程/多进程压测 SET，输出 QPS、P95/P99
- [ ] 基准管理：保存历史结果，形成趋势对比
- [ ] 接入 GitHub Actions：PR/Push 自动运行测试

---

## GitHub Actions

> 下面是一个可直接改造的 CI 示例（按需启用/调整）。  
> 将文件保存为：

```yml
name: tests
```

---

## 配置建议

你可以通过环境变量管理 Redis 地址，便于本地/Docker/CI 统一：

- `REDIS_HOST`（默认 `localhost`）
- `REDIS_PORT`（默认 `6379`）
- `REDIS_DB`（默认 `0`）

---




