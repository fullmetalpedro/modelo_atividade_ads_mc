from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.produto_routes import router as produto_router
from app.routes.login_routes import router as login_router

app = FastAPI(title='KiOferta API', version='1.0')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(produto_router)
app.include_router(login_router)


@app.get('/')
def raiz():
    return {'api': 'KiOferta', 'docs': '/docs'}
