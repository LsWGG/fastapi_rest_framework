import uvicorn

from apps import create_app

app = create_app()  # 创建app

if __name__ == '__main__':
    uvicorn.run('run_api:app', port=8899, host='0.0.0.0', reload=True, proxy_headers=True, debug=True)
