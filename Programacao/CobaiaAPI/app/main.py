# ! Alteração de IA - Revisar
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import admin_fault, pedidos, produtos

app = FastAPI(title="CobaiaAPI", version="0.1.0")

# Sem hardening (allow_origins=["*"]) de propósito — é ambiente de teste,
# consumido por Programacao/CobaiaFront/produtos_api.php (outra origem/porta).
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(produtos.router)
app.include_router(pedidos.router)
app.include_router(admin_fault.router)


@app.get("/", include_in_schema=False)
def root():
    return {"servico": "CobaiaAPI", "docs": "/docs"}
