from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.controllers.login_controller import LoginController

router = APIRouter(prefix='/api/login', tags=['login'])
controller = LoginController()


class Credenciais(BaseModel):
    nome: str
    senha: str


@router.post('')
def entrar(credenciais: Credenciais):
    usuario = controller.autenticar(credenciais.nome, credenciais.senha)
    if usuario is None:
        raise HTTPException(401, 'nome ou senha inválidos')
    return usuario
