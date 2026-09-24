import React from 'react';

export default function SessoesView({ sessoes = [], filmes = [], salas = [], loading, onRefresh }) {
  const getFilmeName = (codigoFilme) => {
    if (!filmes || filmes.length === 0) return `Filme #${codigoFilme}`;
    const f = filmes.find((item) => Number(item.codigo) === Number(codigoFilme));
    return f ? f.nome : `Filme #${codigoFilme}`;
  };

  const getSalaInfo = (numeroSala) => {
    if (!salas || salas.length === 0) return `Sala ${numeroSala}`;
    const s = salas.find((item) => Number(item.numero) === Number(numeroSala));
    return s ? `Sala ${s.numero} (${s.tipo})` : `Sala ${numeroSala}`;
  };

  const formatHour = (hour) => {
    if (hour === undefined || hour === null) return 'N/D';
    const h = String(hour).padStart(2, '0');
    return `${h}:00h`;
  };

  // Helper para calcular assentos seja dict { "1": 0 } ou array [{ ocupado: 0 }]
  const calculateSeats = (assentos) => {
    if (!assentos) return { total: 0, ocupados: 0, livres: 0, percentualLivre: 100 };

    let total = 0;
    let ocupados = 0;

    if (Array.isArray(assentos)) {
      total = assentos.length;
      ocupados = assentos.filter((a) => (typeof a === 'object' ? a.ocupado === 1 : a === 1)).length;
    } else if (typeof assentos === 'object') {
      const entries = Object.values(assentos);
      total = entries.length;
      ocupados = entries.filter((status) => status === 1).length;
    }

    const livres = Math.max(0, total - ocupados);
    const percentualLivre = total > 0 ? Math.round((livres / total) * 100) : 100;

    return { total, ocupados, livres, percentualLivre };
  };

  return (
    <div>
      <div className="hero-header">
        <div className="hero-title-group">
          <h2>Sessões Disponíveis</h2>
          <p>Consumidas diretamente do endpoint <code>/sessoes/</code></p>
        </div>
        <div className="action-buttons">
          <button className="btn btn-secondary" onClick={onRefresh} disabled={loading}>
            Atualizar Sessões
          </button>
        </div>
      </div>

      {loading ? (
        <div className="state-box">
          <div className="state-spinner" />
          <h3 className="state-title">Carregando sessões...</h3>
          <p className="state-description">Buscando as sessões cadastradas na API REST.</p>
        </div>
      ) : sessoes.length === 0 ? (
        <div className="state-box">
          <div style={{ fontSize: '3rem', marginBottom: '1rem' }}></div>
          <h3 className="state-title">Nenhuma sessão agendada no momento</h3>
          <p className="state-description">
            Cadastre novas sessões através do endpoint <code>POST /sessoes/</code>.
          </p>
          <button className="btn btn-primary" onClick={onRefresh}>
            Atualizar
          </button>
        </div>
      ) : (
        <div className="sessions-list">
          {sessoes.map((sessao) => {
            const { total, livres, percentualLivre } = calculateSeats(sessao.assentos);

            return (
              <div key={sessao.codigo} className="session-card">
                <div className="session-header">
                  <span className="session-time-pill">{formatHour(sessao.hora_inicio)}</span>
                  <span className="session-room-badge">{getSalaInfo(sessao.numero_sala)}</span>
                </div>

                <div>
                  <h3 className="session-movie-name">{getFilmeName(sessao.codigo_filme)}</h3>
                  <div className="session-date">Data da Exibição: <strong>{sessao.data}</strong></div>
                  <div style={{ fontSize: '0.85rem', color: 'var(--text-faint)', marginBottom: '0.5rem' }}>
                    Código da Sessão: #{sessao.codigo}
                  </div>
                </div>

                <div className="seats-progress-container">
                  <div className="seats-label">
                    <span>Assentos disponíveis:</span>
                    <strong>{livres} / {total} ({percentualLivre}% livres)</strong>
                  </div>
                  <div className="progress-bar-bg">
                    <div
                      className="progress-bar-fill"
                      style={{ width: `${Math.max(5, percentualLivre)}%` }}
                    />
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
