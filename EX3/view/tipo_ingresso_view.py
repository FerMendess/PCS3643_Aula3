"""REST API endpoints for TipoIngresso resources."""

from __future__ import annotations

from controller.tipo_ingresso_controller import TipoIngressoController
from fastapi import APIRouter, HTTPException, status
from model.tipo_ingresso import (
    TipoIngressoCreate,
    TipoIngressoResponse,
    TipoIngressoUpdate,
)

router = APIRouter(prefix="/tipos-ingresso", tags=["Tipos de Ingresso"])
tipo_ingresso_ctrl = TipoIngressoController()


@router.post(
    "/",
    response_model=TipoIngressoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar ou atualizar tipo e valor de ingresso",
)
def cadastrar_tipo_ingresso_endpoint(
    payload: TipoIngressoCreate,
) -> TipoIngressoResponse:
    sucesso = tipo_ingresso_ctrl.cadastrar_tipo_ingresso(
        tipo_sala=payload.tipo,
        valor_ingresso=payload.valor,
    )
    if not sucesso:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não foi possível cadastrar o tipo de ingresso. Valor deve ser inteiro positivo.",
        )
    return TipoIngressoResponse(tipo=payload.tipo, valor=payload.valor)


@router.get(
    "/",
    response_model=list[TipoIngressoResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar todos os tipos de ingresso",
)
def listar_tipos_ingresso_endpoint() -> list[TipoIngressoResponse]:
    tipos = tipo_ingresso_ctrl.listar_tipos_ingresso()
    return [
        TipoIngressoResponse(tipo=t.tipo, valor=t.valor)
        for t in tipos
        if t.tipo is not None and t.valor is not None
    ]


@router.get(
    "/{tipo}",
    response_model=TipoIngressoResponse,
    status_code=status.HTTP_200_OK,
    summary="Obter detalhes de um tipo de ingresso",
)
def obter_tipo_ingresso_endpoint(tipo: str) -> TipoIngressoResponse:
    tipo_obj = tipo_ingresso_ctrl.buscar_tipo_ingresso(tipo)
    if tipo_obj is None or tipo_obj.tipo is None or tipo_obj.valor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tipo de ingresso '{tipo}' não encontrado.",
        )
    return TipoIngressoResponse(tipo=tipo_obj.tipo, valor=tipo_obj.valor)


@router.put(
    "/{tipo}",
    response_model=TipoIngressoResponse,
    status_code=status.HTTP_200_OK,
    summary="Editar valor de um tipo de ingresso",
)
def editar_tipo_ingresso_endpoint(
    tipo: str, payload: TipoIngressoUpdate
) -> TipoIngressoResponse:
    tipo_obj = tipo_ingresso_ctrl.editar_tipo_ingresso(tipo, payload.valor)
    if tipo_obj is None or tipo_obj.tipo is None or tipo_obj.valor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Não foi possível atualizar o tipo de ingresso '{tipo}'.",
        )
    return TipoIngressoResponse(tipo=tipo_obj.tipo, valor=tipo_obj.valor)


@router.delete(
    "/{tipo}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remover um tipo de ingresso",
)
def remover_tipo_ingresso_endpoint(tipo: str) -> None:
    removido = tipo_ingresso_ctrl.remover_tipo_ingresso(tipo)
    if not removido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tipo de ingresso '{tipo}' não encontrado.",
        )
