import React from 'react';
import { getMoviePoster, getSvgPosterFallback } from '../utils/posters';

export default function FilmesView({ filmes, loading, onRefresh }) {
  const formatDuration = (mins) => {
    if (!mins) return 'N/D';
    const h = Math.floor(mins / 60);
    const m = mins % 60;
    if (h > 0) return `${h}h ${m > 0 ? `${m}m` : ''} (${mins} min)`;
    return `${mins} min`;
  };

  return (
    <div>
      <div className="hero-header">
        <div className="hero-title-group">
          <h2>Filmes em Cartaz</h2>
          <p>Catálogo atualizado em tempo real via endpoint <code>/filmes/</code></p>
        </div>
        <div className="action-buttons">
          <button className="btn btn-secondary" onClick={onRefresh} disabled={loading}>
            Atualizar Catálogo
          </button>
        </div>
      </div>

      {loading ? (
        <div className="state-box">
          <div className="state-spinner" />
          <h3 className="state-title">Carregando catálogo...</h3>
          <p className="state-description">Buscando os filmes cadastrados na API REST.</p>
        </div>
      ) : filmes.length === 0 ? (
        <div className="state-box">
          <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>🎞️</div>
          <h3 className="state-title">Nenhum filme cadastrado no momento</h3>
          <p className="state-description">
            Cadastre novos filmes através da API REST (<code>POST /filmes/</code>) ou via documentação interativa em <code>/docs</code>.
          </p>
          <button className="btn btn-primary" onClick={onRefresh}>
            🔄 Tentar novamente
          </button>
        </div>
      ) : (
        <div className="movie-grid">
          {filmes.map((filme) => (
            <article key={filme.codigo} className="movie-card">
              <div className="poster-wrapper">
                <span className="code-badge">ID #{filme.codigo}</span>
                <span className="duration-badge">{filme.duracao} min</span>
                <img
                  src={getMoviePoster(filme)}
                  alt={`Cartaz do filme ${filme.nome}`}
                  className="poster-img"
                  loading="lazy"
                  onError={(e) => {
                    e.currentTarget.onerror = null;
                    e.currentTarget.src = getSvgPosterFallback(filme.nome);
                  }}
                />
                <div className="poster-overlay" />
              </div>

              <div className="movie-body">
                <h3 className="movie-title">{filme.nome}</h3>

                <div className="movie-info-row">
                  <span className="movie-info-label"> Duração:</span>
                  <span className="movie-info-value">{formatDuration(filme.duracao)}</span>
                </div>

                <div className="movie-info-row">
                  <span className="movie-info-label"> Estreia:</span>
                  <span className="movie-info-value">{filme.data_estreia}</span>
                </div>

                <div className="movie-info-row">
                  <span className="movie-info-label"> Encerramento:</span>
                  <span className="movie-info-value">{filme.data_saida}</span>
                </div>
              </div>
            </article>
          ))}
        </div>
      )}
    </div>
  );
}
