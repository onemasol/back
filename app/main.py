from fastapi import FastAPI, Depends
from app.core.config import settings
from app.api.v1.router import router as api_v1_router
from app.db.session import init_db
from dotenv import load_dotenv
load_dotenv(".env")  # 반드시 Settings() 보다 먼저 호출해야 합니다.
from app.core.config import settings
from app.core.custom_response import CustomJSONResponse
from app.api.v1.deps import http_bearer_scheme
def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version="0.1.0",
        description="자영업자 비서형 캘린더 + AI 에이전트",
        default_response_class=CustomJSONResponse,
        #dependencies=[Depends(http_bearer_scheme)] # <<< 2. 앱 생성자에 이 부분을 추가합니다.
    )
   

    # 라우터
    app.include_router(api_v1_router, prefix=settings.API_V1_STR)
    return app

app = create_app()

@app.on_event("startup")
async def on_startup():
    await init_db()   # ← 여기에 테이블 생성 호출

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

@app.get("/")
def read_root():
    return {"message": "Welcome to Onemasol API"}