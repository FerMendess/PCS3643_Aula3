"""REST API endpoints for Sala resources."""

from __future__ import annotations

from controller.sala_controller import SalaController
from fastapi import APIRouter, HTTPException, status
from model.sala import SalaCreate, SalaResponse, SalaUpdate

router = APIRouter(prefix="/salas", tags=["Salas"])
sala_ctrl = SalaController()


@router.post(
    "/",
    response_model=SalaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar uma nova sala",
)
def cadastrar_sala_endpoint(payload: SalaCreate) -> SalaResponse:
    sala = sala_ctrl.cadastrar_sala(
        numero=payload.numero,
        capacidade=payload.capacidade,
        tipo_sala=payload.tipo,
    )
    if sala is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Dados inválidos ou sala com mesmo número já cadastrada.",
        )
    return SalaResponse(
        numero=sala.numero,
        capacidade=sala.capacidade,
        tipo=sala.tipo,
    )


@router.get(
    "/",
    response_model=list[SalaResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar todas as salas",
)
def listar_salas_endpoint() -> list[SalaResponse]:
    salas = sala_ctrl.listar_salas()
    return [
        SalaResponse(
            numero=s.numero,
            capacidade=s.capacidade,
            tipo=s.tipo,
        )
        for s in salas
        if s.numero is not None and s.capacidade is not None and s.tipo is not None
    ]


@router.get(
    "/{numero}",
    response_model=SalaResponse,
    status_code=status.HTTP_200_OK,
    summary="Obter detalhes de uma sala",
)
def obter_sala_endpoint(numero: int) -> SalaResponse:
    sala = sala_ctrl.buscar_sala(numero)
    if sala is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sala com número {numero} não encontrada.",
        )
    return SalaResponse(
        numero=sala.numero,
        capacidade=sala.capacidade,
        tipo=sala.tipo,
    )


@router.put(
    "/{numero}",
    response_model=SalaResponse,
    status_code=status.HTTP_200_OK,
    summary="Editar dados de uma sala",
)
def editar_sala_endpoint(numero: int, payload: SalaUpdate) -> SalaResponse:
    sala = sala_ctrl.editar_sala(
        numero=numero,
        capacidade=payload.capacidade,
        tipo=payload.tipo,
    )
    if sala is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não foi possível atualizar a sala. Verifique os dados fornecidos.",
        )
    return SalaResponse(
        numero=sala.numero,
        capacidade=sala.capacidade,
        tipo=sala.tipo,
    )


@router.delete(
    "/{numero}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remover uma sala",
)
def remover_sala_endpoint(numero: int) -> None:
    removido = sala_ctrl.remover_sala(numero)
    if not removido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sala {numero} não encontrada ou possui sessões vinculadas.",
        )
