from fastapi import FastAPI
from modulos.sistema import asegurados, polizas
from modulos.web import web_asegurados as asegurados_web
import auth

app = FastAPI()

# Auth
app.include_router(auth.router, prefix="/auth", tags=["Autenticación"])

# Sistema
app.include_router(asegurados.router, prefix="/api/asegurados", tags=["Asegurados"])
app.include_router(polizas.router, prefix="/api/polizas", tags=["Pólizas"])

#Web
app.include_router(asegurados_web.router, prefix="/api/web/asegurados", tags=["Web Asegurados"])


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
