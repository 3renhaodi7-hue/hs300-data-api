# api/stockdata.py - 最简Vercel Serverless函数
import json

def main(request, response):
    # 构建响应数据
    data = {
        "message": "Hello from Vercel Serverless Function!",
        "success": True
    }
    # 设置响应头
    response.set_header('Content-Type', 'application/json')
    # 返回响应
    response.set_body(json.dumps(data))
    return response
