- 客户端发准备消息
    - {"op": "prepare", "data": {}}
    - 如果访问的token有错，返回{"status": "error", "data": {}}

- 服务端发轮到消息
    - {"status": "wait", "data": "这里是游戏jar传出来的一段json数据"}

- 客户端发操作消息
    - {"op": "operation", data: "这里是本地AI的json格式的运行结果，需要喂给服务器的游戏jar"}

- 服务器发结束消息
    - {"status": "win", data: {}}
    - {"status": "lose", data: {}}
    - {"status": "draw", data: {}}

- 客户端有可能会发一个不合法的操作，那服务端就返回
    - {"status": "wrong", data: "这里是游戏jar传出来的一段json数据"}
    - 然后等客户端再发一个操作