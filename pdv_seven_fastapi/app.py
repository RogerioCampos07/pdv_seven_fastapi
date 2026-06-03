from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from pdv_seven_fastapi.database import get_session
from pdv_seven_fastapi.estoque.models import (
    Categoria,
)
from pdv_seven_fastapi.estoque.schema import (
    CategoriaSchema,
)

app = FastAPI(title='Loja Seven')


@app.get('/')
def read_root():
    return {'Hello': 'World'}


@app.post(
    '/estoque/categorias',
    response_model=CategoriaSchema,
    status_code=HTTPStatus.CREATED,
)
def create_categorias(
    categoria: CategoriaSchema, session: Session = Depends(get_session)
):
    db_categoria = session.scalar(
        select(Categoria).where((Categoria.nome == categoria.nome))
    )
    if db_categoria:
        if db_categoria.nome == categoria.nome:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT, detail='Categoria já existe'
            )

    db_categoria = Categoria(nome=categoria.nome)

    session.add(db_categoria)
    session.commit()
    session.refresh(db_categoria)

    return db_categoria
