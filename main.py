from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
import uvicorn

app = FastAPI()

# 預設轉址位址（可依需求修改）
redirect_url = "https://google.com"

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """
    首頁，顯示目前設定的轉址位址，
    並提供連結到設定頁面與轉址測試頁面。
    """
    html_content = f"""
    <html>
        <head>
            <meta charset="utf-8">
            <title>轉址服務首頁</title>
        </head>
        <body>
            <h1>轉址服務首頁</h1>
            <p>目前設定的轉址位址：<strong>{redirect_url}</strong></p>
            <p>
                <a href="/set">設定轉址位址</a>
            </p>
            <p>
                點選此連結測試 <a href="/redirect">302 轉址</a>
            </p>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/set", response_class=HTMLResponse)
async def set_get(request: Request):
    """
    以 GET 方法顯示設定轉址位址的表單。
    """
    html_content = f"""
    <html>
        <head>
            <meta charset="utf-8">
            <title>設定轉址位址</title>
        </head>
        <body>
            <h1>設定轉址位址</h1>
            <form action="/set" method="post">
                <label for="url">轉址位址：</label>
                <input type="text" id="url" name="url" value="{redirect_url}" required>
                <button type="submit">更新</button>
            </form>
            <p><a href="/">回首頁</a></p>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.post("/set", response_class=HTMLResponse)
async def set_post(request: Request, url: str = Form(...)):
    """
    以 POST 方法處理表單提交，更新全域變數 redirect_url。
    """
    global redirect_url
    redirect_url = url  # 更新轉址位址

    html_content = f"""
    <html>
        <head>
            <meta charset="utf-8">
            <title>轉址位址已更新</title>
        </head>
        <body>
            <h1>轉址位址已更新</h1>
            <p>目前設定的轉址位址：<strong>{redirect_url}</strong></p>
            <p><a href="/">回首頁</a></p>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/redirect")
async def do_redirect():
    """
    以 302 狀態碼自動轉址到目前設定的 redirect_url。
    """
    return RedirectResponse(url=redirect_url, status_code=302)

if __name__ == "__main__":
    # 啟動 uvicorn 伺服器，監聽在 127.0.0.1:8000
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
