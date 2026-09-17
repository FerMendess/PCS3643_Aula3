"""REST API endpoints for Sessao and Ticket purchase operations."""

from fastapi import APIRouter, Depends, HTTPException, status

from src.controller.sessao_controller import SessaoController
from src.model.sessao import (
    CompraIngressoRequest,
    CompraIngressoResponse,
    Sessao,
    SessaoCreate,
    SessaoDisponivelResponse,
    SessaoResponse,
    SessaoUpdate,
)

router = APIRouter(prefix="/sessoes", tags=["Sessões"])


def get_sessao_controller() -> SessaoController:
    return SessaoController()


def _to_sessao_response(sessao: Sessao) -> SessaoResponse:
    return SessaoResponse(
        codigo=sessao.codigo or 0,
        numero_sala=sessao.sala.numero if sessao.sala and sessao.sala.numero else 0,
        codigo_filme=sessao.filme.codigo if sessao.filme and sessao.filme.codigo else 0,
        data=sessao.data or "",
        hora_inicio=sessao.hora_inicio or 0,
        assentos=sessao.assentos,
    )


@router.post(
    "/",
    response_model=SessaoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar uma nova sessão",
)
def cadastrar_sessao_endpoint(
    payload: SessaoCreate,
    ctrl: SessaoController = Depends(get_sessao_controller),
) -> SessaoResponse:
    sessao = ctrl.cadastrar_sessao(
        numero_sala=payload.numero_sala,
        codigo_filme=payload.codigo_filme,
        data_sessao=payload.data,
        hora_inicio=payload.hora_inicio,
    )
    if (
        sessao is None
        or sessao.codigo is None
        or sessao.sala is None
        or sessao.filme is None
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não foi possível cadastrar a sessão. Verifique sala, filme, data e conflitos de horário.",
        )
    return _to_sessao_response(sessao)


@router.get(
    "/",
    response_model=list[SessaoResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar todas as sessões",
)
def listar_sessoes_endpoint(
    ctrl: SessaoController = Depends(get_sessao_controller),
) -> list[SessaoResponse]:
    sessoes = ctrl.listar_sessoes()
    return [_to_sessao_response(s) for s in sessoes]


@router.get(
    "/data/{data_str:path}",
    response_model=list[SessaoDisponivelResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar sessões disponíveis para uma determinada data (DD/MM/AAAA)",
)
def listar_sessoes_por_data_endpoint(
    data_str: str,
    ctrl: SessaoController = Depends(get_sessao_controller),
) -> list[SessaoDisponivelResponse]:
    itens = ctrl.listar_filmes_por_data_detalhado(data_str)
    return [
        SessaoDisponivelResponse(
            codigo=item["codigo"],
            filme_nome=item["filme_nome"],
            numero_sala=item["numero_sala"],
            tipo_sala=item["tipo_sala"],
            hora_inicio=item["hora_inicio"],
            valor=item["valor"],
            descricao=item["descricao"],
        )
        for item in itens
    ]


@router.get(
    "/{codigo}",
    response_model=SessaoResponse,
    status_code=status.HTTP_200_OK,
    summary="Obter detalhes e mapa de assentos de uma sessão",
)
def obter_sessao_endpoint(
    codigo: int,
    ctrl: SessaoController = Depends(get_sessao_controller),
) -> SessaoResponse:
    sessao = ctrl.buscar_sessao(codigo)
    if sessao is None or sessao.codigo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sessão com código {codigo} não encontrada.",
        )
    return _to_sessao_response(sessao)


@router.put(
    "/{codigo}",
    response_model=SessaoResponse,
    status_code=status.HTTP_200_OK,
    summary="Editar dados de uma sessão",
)
def editar_sessao_endpoint(
    codigo: int,
    payload: SessaoUpdate,
    ctrl: SessaoController = Depends(get_sessao_controller),
) -> SessaoResponse:
    sessao = ctrl.editar_sessao(
        codigo=codigo,
        numero_sala=payload.numero_sala,
        codigo_filme=payload.codigo_filme,
        data=payload.data,
        hora_inicio=payload.hora_inicio,
    )
    if sessao is None or sessao.codigo is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não foi possível atualizar a sessão. Verifique os dados e conflitos.",
        )
    return _to_sessao_response(sessao)


@router.delete(
    "/{codigo}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remover uma sessão",
)
def remover_sessao_endpoint(
    codigo: int,
    ctrl: SessaoController = Depends(get_sessao_controller),
) -> None:
    removido = ctrl.remover_sessao(codigo)
    if not removido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sessão com código {codigo} não encontrada.",
        )


@router.post(
    "/{codigo}/comprar",
    response_model=CompraIngressoResponse,
    status_code=status.HTTP_200_OK,
    summary="Comprar ingressos para uma sessão",
)
def comprar_ingressos_endpoint(
    codigo: int,
    payload: CompraIngressoRequest,
    ctrl: SessaoController = Depends(get_sessao_controller),
) -> CompraIngressoResponse:
    total = ctrl.comprar_ingressos(
        codigo_sessao=codigo,
        assentos=payload.assentos,
        tipos_ingresso=payload.tipos_ingresso,
    )
    if total <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Falha ao comprar ingressos. Verifique se os assentos estão livres e os tipos são válidos.",
        )
    return CompraIngressoResponse(
        codigo_sessao=codigo,
        assentos_comprados=payload.assentos,
        total=total,
    )
