from pydantic import BaseModel, Field
from typing import Optional

class ProductBoundary(BaseModel):
    id: str = Field(description="Identificador único del límite (ej. backend, frontend, auth-service)")
    path: str = Field(description="Ruta relativa desde la raíz del repositorio")
    language: str = Field(description="Lenguaje principal (ej. Python, TypeScript, Rust)")
    framework: Optional[str] = Field(None, description="Framework detectado (ej. React, FastAPI, Express)")
    role: str = Field(description="Rol del límite en el proyecto (ej. frontend, backend, sdk, docs)")
