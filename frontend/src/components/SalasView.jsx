import React from 'react';

export default function SalasView({ salas, loading, onRefresh }) {
  const getBadgeClass = (tipo) => {
    const t = (tipo || '').toUpperCase();
    if (t.includes('IMAX')) return 'imax';
    if (t.includes('3D')) return 'three-d';
    return 'two-d';
  };

  return (
    <div>
      <div className="hero-header">
        <div className="hero-title-group">
          <h2>Salas de Exibição</h2>
          <p>Informações de capacidade e tecnologia de projeção via <code>/salas/</code></p>
        </div>
        <div className="action-buttons">
          <button className="btn btn-secondary" onClick={onRefresh} disabled={loading}>
            Atualizar Salas
          </button>
        </div>
      </div>

      {loading ? (
        <div className="state-box">
          <div className="state-spinner" />
          <h3 className="state-title">Carregando salas...</h3>
          <p className="state-description">Buscando as salas cadastradas na API REST.</p>
        </div>
      ) : salas.length === 0 ? (
        <div className="state-box">
          <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>🏛️</div>
          <h3 className="state-title">Nenhuma sala cadastrada no momento</h3>
          <p className="state-description">
            Cadastre novas salas através do endpoint <code>POST /salas/</code>.
          </p>
          <button className="btn btn-primary" onClick={onRefresh}>
            Atualizar
          </button>
        </div>
      ) : (
        <div className="rooms-grid">
          {salas.map((sala) => (
            <div key={sala.numero} className="room-card">
              <div className="room-top">
                <span className="room-number">Sala {sala.numero}</span>
                <span className={`room-badge-type ${getBadgeClass(sala.tipo)}`}>
                  {sala.tipo}
                </span>
              </div>

              <div className="room-capacity">
                <span> Capacidade Total:</span>
                <strong>{sala.capacidade} lugares</strong>
              </div>

              <div style={{ marginTop: '1.25rem', paddingTop: '1rem', borderTop: '1px solid rgba(255,255,255,0.06)' }}>
                <p style={{ fontSize: '0.88rem', color: 'var(--text-muted)' }}>
                  {sala.tipo.toUpperCase() === 'IMAX' && 'Projeção imersiva com tela de alta escala e som espacial potente.'}
                  {sala.tipo.toUpperCase() === '3D' && 'Tecnologia de profundidade estereoscópica e óculos polarizados.'}
                  {sala.tipo.toUpperCase() === '2D' && 'Projeção digital padrão com alta definição e conforto acústico.'}
                </p>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
