"""REST API endpoints for TipoIngresso resources."""

from fastapi import APIRouter, Depends, HTTPException, status

from src.controller.tipo_ingresso_controller import TipoIngressoController
from src.model.tipo_ingresso import (
    TipoIngressoCreate,
    TipoIngressoResponse,
    TipoIngressoUpdate,
)

router = APIRouter(prefix="/tipos-ingresso", tags=["Tipos de Ingresso"])


def get_tipo_ingresso_controller() -> TipoIngressoController:
    return TipoIngressoController()


@router.post(
    "/",
    response_model=TipoIngressoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar ou atualizar tipo e valor de ingresso",
)
def cadastrar_tipo_ingresso_endpoint(
    payload: TipoIngressoCreate,
    ctrl: TipoIngressoController = Depends(get_tipo_ingresso_controller),
) -> TipoIngressoResponse:
    sucesso = ctrl.cadastrar_tipo_ingresso(
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
def listar_tipos_ingresso_endpoint(
    ctrl: TipoIngressoController = Depends(get_tipo_ingresso_controller),
) -> list[TipoIngressoResponse]:
    tipos = ctrl.listar_tipos_ingresso()
    return [TipoIngressoResponse.model_validate(t) for t in tipos]


@router.get(
    "/{tipo}",
    response_model=TipoIngressoResponse,
    status_code=status.HTTP_200_OK,
    summary="Obter detalhes de um tipo de ingresso",
)
def obter_tipo_ingresso_endpoint(
    tipo: str,
    ctrl: TipoIngressoController = Depends(get_tipo_ingresso_controller),
) -> TipoIngressoResponse:
    tipo_obj = ctrl.buscar_tipo_ingresso(tipo)
    if tipo_obj is None or tipo_obj.tipo is None or tipo_obj.valor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tipo de ingresso '{tipo}' não encontrado.",
        )
    return TipoIngressoResponse.model_validate(tipo_obj)


@router.put(
    "/{tipo}",
    response_model=TipoIngressoResponse,
    status_code=status.HTTP_200_OK,
    summary="Editar valor de um tipo de ingresso",
)
def editar_tipo_ingresso_endpoint(
    tipo: str,
    payload: TipoIngressoUpdate,
    ctrl: TipoIngressoController = Depends(get_tipo_ingresso_controller),
) -> TipoIngressoResponse:
    tipo_obj = ctrl.editar_tipo_ingresso(tipo, payload.valor)
    if tipo_obj is None or tipo_obj.tipo is None or tipo_obj.valor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Não foi possível atualizar o tipo de ingresso '{tipo}'.",
        )
    return TipoIngressoResponse.model_validate(tipo_obj)


@router.delete(
    "/{tipo}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remover um tipo de ingresso",
)
def remover_tipo_ingresso_endpoint(
    tipo: str,
    ctrl: TipoIngressoController = Depends(get_tipo_ingresso_controller),
) -> None:
    removido = ctrl.remover_tipo_ingresso(tipo)
    if not removido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tipo de ingresso '{tipo}' não encontrado.",
        )
