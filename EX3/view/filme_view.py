"""REST API endpoints for Filme resources."""

from __future__ import annotations

from controller.filme_controller import FilmeController
from fastapi import APIRouter, HTTPException, status
from model.filme import FilmeCreate, FilmeResponse, FilmeUpdate

router = APIRouter(prefix="/filmes", tags=["Filmes"])
filme_ctrl = FilmeController()


@router.post(
    "/",
    response_model=FilmeResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar um novo filme",
)
def cadastrar_filme_endpoint(payload: FilmeCreate) -> FilmeResponse:
    filme = filme_ctrl.cadastrar_filme(
        nome=payload.nome,
        data_estreia=payload.data_estreia,
        data_saida=payload.data_saida,
        duracao=payload.duracao,
    )
    if filme is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Dados inválidos ou filme com mesmo nome já cadastrado.",
        )
    return FilmeResponse(
        codigo=filme.codigo,
        nome=filme.nome,
        data_estreia=filme.data_estreia,
        data_saida=filme.data_saida,
        duracao=filme.duracao,
    )


@router.get(
    "/",
    response_model=list[FilmeResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar todos os filmes",
)
def listar_filmes_endpoint() -> list[FilmeResponse]:
    filmes = filme_ctrl.listar_filmes()
    return [
        FilmeResponse(
            codigo=f.codigo,
            nome=f.nome,
            data_estreia=f.data_estreia,
            data_saida=f.data_saida,
            duracao=f.duracao,
        )
        for f in filmes
        if f.codigo is not None
        and f.nome is not None
        and f.data_estreia is not None
        and f.data_saida is not None
        and f.duracao is not None
    ]


@router.get(
    "/{codigo}",
    response_model=FilmeResponse,
    status_code=status.HTTP_200_OK,
    summary="Obter detalhes de um filme",
)
def obter_filme_endpoint(codigo: int) -> FilmeResponse:
    filme = filme_ctrl.buscar_filme(codigo)
    if filme is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Filme com código {codigo} não encontrado.",
        )
    return FilmeResponse(
        codigo=filme.codigo,
        nome=filme.nome,
        data_estreia=filme.data_estreia,
        data_saida=filme.data_saida,
        duracao=filme.duracao,
    )


@router.put(
    "/{codigo}",
    response_model=FilmeResponse,
    status_code=status.HTTP_200_OK,
    summary="Editar dados de um filme",
)
def editar_filme_endpoint(codigo: int, payload: FilmeUpdate) -> FilmeResponse:
    filme = filme_ctrl.editar_filme(
        codigo=codigo,
        nome=payload.nome,
        data_estreia=payload.data_estreia,
        data_saida=payload.data_saida,
        duracao=payload.duracao,
    )
    if filme is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não foi possível atualizar o filme. Verifique se o código existe e os dados são válidos.",
        )
    return FilmeResponse(
        codigo=filme.codigo,
        nome=filme.nome,
        data_estreia=filme.data_estreia,
        data_saida=filme.data_saida,
        duracao=filme.duracao,
    )


@router.delete(
    "/{codigo}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remover um filme",
)
def remover_filme_endpoint(codigo: int) -> None:
    removido = filme_ctrl.remover_filme(codigo)
    if not removido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Filme com código {codigo} não encontrado ou possui sessões vinculadas.",
        )
