# ! Alteração de IA - Revisar: aplicação FastAPI da CobaiaAPI — registra os routers de
# produto, pedido e controle de falhas, e libera CORS para qualquer origem.
# ! Motivo: a página produtos_api.php é servida pelo PHP na porta 8080 e consome esta API
# na 8000 — origem diferente, então sem CORS liberado o navegador bloquearia o fetch e o
# alvo "moderno" não geraria tráfego nenhum para o agente interceptar. Sem restrição de
# origem porque é ambiente de teste sem dado real, não um serviço exposto.
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
