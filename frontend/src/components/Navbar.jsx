import React from 'react';

export default function Navbar({ activeTab, onSelectTab, apiOnline }) {
  const tabs = [
    { id: 'filmes', label: 'Filmes em Cartaz' },
    { id: 'sessoes', label: 'Sessões' },
    { id: 'salas', label: 'Salas' },
    { id: 'ingressos', label: 'Tipos de Ingresso' },
  ];

  return (
    <header className="navbar">
      <div className="brand" onClick={() => onSelectTab('filmes')}>
        <div className="brand-icon">🍿</div>
        <span className="brand-title">CineMax</span>
      </div>

      <nav className="nav-links">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            className={`nav-item ${activeTab === tab.id ? 'active' : ''}`}
            onClick={() => onSelectTab(tab.id)}
          >
            {tab.label}
          </button>
        ))}
      </nav>

      <div className="api-badge">
        <span className={`status-dot ${apiOnline ? 'online' : 'offline'}`} />
        <span>{apiOnline ? 'API Conectada' : 'API Desconectada'}</span>
      </div>
    </header>
  );
}
