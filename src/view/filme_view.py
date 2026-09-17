"""REST API endpoints for Filme resources."""

from fastapi import APIRouter, Depends, HTTPException, status

from controller.filme_controller import FilmeController
from model.filme import FilmeCreate, FilmeResponse, FilmeUpdate

router = APIRouter(prefix="/filmes", tags=["Filmes"])


def get_filme_controller() -> FilmeController:
    return FilmeController()


@router.post(
    "/",
    response_model=FilmeResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar um novo filme",
)
def cadastrar_filme_endpoint(
    payload: FilmeCreate,
    ctrl: FilmeController = Depends(get_filme_controller),
) -> FilmeResponse:
    filme = ctrl.cadastrar_filme(
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
    return FilmeResponse.model_validate(filme)


@router.get(
    "/",
    response_model=list[FilmeResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar todos os filmes",
)
def listar_filmes_endpoint(
    ctrl: FilmeController = Depends(get_filme_controller),
) -> list[FilmeResponse]:
    filmes = ctrl.listar_filmes()
    return [FilmeResponse.model_validate(f) for f in filmes]


@router.get(
    "/{codigo}",
    response_model=FilmeResponse,
    status_code=status.HTTP_200_OK,
    summary="Obter detalhes de um filme",
)
def obter_filme_endpoint(
    codigo: int,
    ctrl: FilmeController = Depends(get_filme_controller),
) -> FilmeResponse:
    filme = ctrl.buscar_filme(codigo)
    if filme is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Filme com código {codigo} não encontrado.",
        )
    return FilmeResponse.model_validate(filme)


@router.put(
    "/{codigo}",
    response_model=FilmeResponse,
    status_code=status.HTTP_200_OK,
    summary="Editar dados de um filme",
)
def editar_filme_endpoint(
    codigo: int,
    payload: FilmeUpdate,
    ctrl: FilmeController = Depends(get_filme_controller),
) -> FilmeResponse:
    filme = ctrl.editar_filme(
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
    return FilmeResponse.model_validate(filme)


@router.delete(
    "/{codigo}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remover um filme",
)
def remover_filme_endpoint(
    codigo: int,
    ctrl: FilmeController = Depends(get_filme_controller),
) -> None:
    removido = ctrl.remover_filme(codigo)
    if not removido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Filme com código {codigo} não encontrado ou possui sessões vinculadas.",
        )
