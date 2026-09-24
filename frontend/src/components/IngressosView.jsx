import React from 'react';

export default function IngressosView({ tiposIngresso, loading, onRefresh }) {
  const formatCurrency = (val) => {
    return Number(val).toLocaleString('pt-BR', {
      style: 'currency',
      currency: 'BRL',
    });
  };

  return (
    <div>
      <div className="hero-header">
        <div className="hero-title-group">
          <h2>Tipos de Ingresso e Valores</h2>
          <p>Tabela de preços cadastrada consumida via <code>/tipos-ingresso/</code></p>
        </div>
        <div className="action-buttons">
          <button className="btn btn-secondary" onClick={onRefresh} disabled={loading}>
            Atualizar Preços
          </button>
        </div>
      </div>

      {loading ? (
        <div className="state-box">
          <div className="state-spinner" />
          <h3 className="state-title">Carregando tipos de ingresso...</h3>
          <p className="state-description">Buscando os tipos cadastrados na API REST.</p>
        </div>
      ) : tiposIngresso.length === 0 ? (
        <div className="state-box">
          <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>🎟️</div>
          <h3 className="state-title">Nenhum tipo de ingresso cadastrado no momento</h3>
          <p className="state-description">
            Cadastre novos valores através do endpoint <code>POST /tipos-ingresso/</code>.
          </p>
          <button className="btn btn-primary" onClick={onRefresh}>
            Atualizar
          </button>
        </div>
      ) : (
        <div className="tickets-grid">
          {tiposIngresso.map((item) => (
            <div key={item.tipo} className="ticket-card">
              <h3 className="ticket-type-title">Sessão {item.tipo}</h3>
              <div className="ticket-price-box">
                <span className="ticket-price-currency">R$</span>
                <span className="ticket-price-amount">{item.valor}</span>
                <span style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>,00</span>
              </div>

              <div style={{ padding: '0.3rem 0.8rem', background: 'rgba(255,255,255,0.06)', borderRadius: '999px', display: 'inline-block', fontSize: '0.85rem', color: '#38bdf8' }}>
                Entrada Inteira: {formatCurrency(item.valor)}
              </div>

              <div style={{ marginTop: '0.5rem', fontSize: '0.85rem', color: 'var(--text-muted)' }}>
                Meia-entrada: {formatCurrency(item.valor / 2)}
              </div>

              <ul className="ticket-features">
                <li> Assento individual numerado</li>
                <li> Acesso à sala de projeção correspondente</li>
                <li> Áudio imersivo de alta fidelidade</li>
                <li> Válido para a sessão selecionada</li>
              </ul>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
