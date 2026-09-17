"""REST API endpoints for Sala resources."""

from fastapi import APIRouter, Depends, HTTPException, status

from controller.sala_controller import SalaController
from model.sala import SalaCreate, SalaResponse, SalaUpdate

router = APIRouter(prefix="/salas", tags=["Salas"])


def get_sala_controller() -> SalaController:
    return SalaController()


@router.post(
    "/",
    response_model=SalaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar uma nova sala",
)
def cadastrar_sala_endpoint(
    payload: SalaCreate,
    ctrl: SalaController = Depends(get_sala_controller),
) -> SalaResponse:
    sala = ctrl.cadastrar_sala(
        numero=payload.numero,
        capacidade=payload.capacidade,
        tipo_sala=payload.tipo,
    )
    if sala is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Dados inválidos ou sala com mesmo número já cadastrada.",
        )
    return SalaResponse.model_validate(sala)


@router.get(
    "/",
    response_model=list[SalaResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar todas as salas",
)
def listar_salas_endpoint(
    ctrl: SalaController = Depends(get_sala_controller),
) -> list[SalaResponse]:
    salas = ctrl.listar_salas()
    return [SalaResponse.model_validate(s) for s in salas]


@router.get(
    "/{numero}",
    response_model=SalaResponse,
    status_code=status.HTTP_200_OK,
    summary="Obter detalhes de uma sala",
)
def obter_sala_endpoint(
    numero: int,
    ctrl: SalaController = Depends(get_sala_controller),
) -> SalaResponse:
    sala = ctrl.buscar_sala(numero)
    if sala is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sala com número {numero} não encontrada.",
        )
    return SalaResponse.model_validate(sala)


@router.put(
    "/{numero}",
    response_model=SalaResponse,
    status_code=status.HTTP_200_OK,
    summary="Editar dados de uma sala",
)
def editar_sala_endpoint(
    numero: int,
    payload: SalaUpdate,
    ctrl: SalaController = Depends(get_sala_controller),
) -> SalaResponse:
    sala = ctrl.editar_sala(
        numero=numero,
        capacidade=payload.capacidade,
        tipo=payload.tipo,
    )
    if sala is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não foi possível atualizar a sala. Verifique os dados fornecidos.",
        )
    return SalaResponse.model_validate(sala)


@router.delete(
    "/{numero}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remover uma sala",
)
def remover_sala_endpoint(
    numero: int,
    ctrl: SalaController = Depends(get_sala_controller),
) -> None:
    removido = ctrl.remover_sala(numero)
    if not removido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sala {numero} não encontrada ou possui sessões vinculadas.",
        )
