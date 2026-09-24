import React, { useState, useEffect, useCallback } from 'react';
import Navbar from './components/Navbar';
import FilmesView from './components/FilmesView';
import SessoesView from './components/SessoesView';
import SalasView from './components/SalasView';
import IngressosView from './components/IngressosView';
import {
  fetchFilmes,
  fetchSalas,
  fetchTiposIngresso,
  fetchSessoes,
  fetchStatus,
} from './services/api';

export default function App() {
  const [activeTab, setActiveTab] = useState('filmes');
  const [apiOnline, setApiOnline] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [filmes, setFilmes] = useState([]);
  const [salas, setSalas] = useState([]);
  const [tiposIngresso, setTiposIngresso] = useState([]);
  const [sessoes, setSessoes] = useState([]);
  const [seeding, setSeeding] = useState(false);

  const loadData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      await fetchStatus();
      setApiOnline(true);

      const [filmesData, salasData, tiposData, sessoesData] = await Promise.all([
        fetchFilmes().catch(() => []),
        fetchSalas().catch(() => []),
        fetchTiposIngresso().catch(() => []),
        fetchSessoes().catch(() => []),
      ]);

      setFilmes(filmesData);
      setSalas(salasData);
      setTiposIngresso(tiposData);
      setSessoes(sessoesData);
    } catch (err) {
      console.warn('Falha ao conectar com o backend FastAPI:', err);
      setApiOnline(false);
      setError(
        'Não foi possível conectar à API REST em http://127.0.0.1:8000. ' +
        'Certifique-se de que o servidor backend está rodando com: python app.py'
      );
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadData();
  }, [loadData]);

  // Função para semear dados de teste caso o banco esteja limpo
  const handleSeedDemoData = async () => {
    setSeeding(true);
    try {
      // 1. Cadastrar tipos de ingresso
      await fetch('http://127.0.0.1:8000/tipos-ingresso/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ tipo: 'IMAX', valor: 50 }),
      }).catch(() => { });

      await fetch('http://127.0.0.1:8000/tipos-ingresso/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ tipo: '3D', valor: 40 }),
      }).catch(() => { });

      await fetch('http://127.0.0.1:8000/tipos-ingresso/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ tipo: '2D', valor: 30 }),
      }).catch(() => { });

      // 2. Cadastrar salas
      await fetch('http://127.0.0.1:8000/salas/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ numero: 1, capacidade: 80, tipo: 'IMAX' }),
      }).catch(() => { });

      await fetch('http://127.0.0.1:8000/salas/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ numero: 2, capacidade: 60, tipo: '3D' }),
      }).catch(() => { });

      await fetch('http://127.0.0.1:8000/salas/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ numero: 3, capacidade: 100, tipo: '2D' }),
      }).catch(() => { });

      // 3. Cadastrar filmes
      const f1Res = await fetch('http://127.0.0.1:8000/filmes/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          nome: 'Duna: Parte 2',
          data_estreia: '01/03/2026',
          data_saida: '30/05/2026',
          duracao: 166,
        }),
      }).then((r) => r.json()).catch(() => null);

      const f2Res = await fetch('http://127.0.0.1:8000/filmes/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          nome: 'Oppenheimer',
          data_estreia: '10/02/2026',
          data_saida: '28/05/2026',
          duracao: 180,
        }),
      }).then((r) => r.json()).catch(() => null);

      const f3Res = await fetch('http://127.0.0.1:8000/filmes/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          nome: 'Interestelar',
          data_estreia: '15/01/2026',
          data_saida: '15/06/2026',
          duracao: 169,
        }),
      }).then((r) => r.json()).catch(() => null);

      // 4. Cadastrar sessões
      const codigoDuna = f1Res?.codigo || 1;
      const codigoOpp = f2Res?.codigo || 2;
      const codigoInter = f3Res?.codigo || 3;

      await fetch('http://127.0.0.1:8000/sessoes/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          numero_sala: 1,
          codigo_filme: codigoDuna,
          data: '25/09/2026',
          hora_inicio: 19,
        }),
      }).catch(() => { });

      await fetch('http://127.0.0.1:8000/sessoes/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          numero_sala: 2,
          codigo_filme: codigoOpp,
          data: '25/09/2026',
          hora_inicio: 21,
        }),
      }).catch(() => { });

      await fetch('http://127.0.0.1:8000/sessoes/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          numero_sala: 3,
          codigo_filme: codigoInter,
          data: '26/09/2026',
          hora_inicio: 18,
        }),
      }).catch(() => { });

      await loadData();
    } catch (err) {
      console.error('Erro ao semear dados:', err);
    } finally {
      setSeeding(false);
    }
  };

  return (
    <div className="app-container">
      <Navbar
        activeTab={activeTab}
        onSelectTab={setActiveTab}
        apiOnline={apiOnline}
      />

      <main className="main-content">
        {error && (
          <div
            style={{
              padding: '1.25rem 1.5rem',
              marginBottom: '2rem',
              backgroundColor: 'rgba(239, 68, 68, 0.15)',
              border: '1px solid rgba(239, 68, 68, 0.4)',
              borderRadius: 'var(--radius-md)',
              color: '#fca5a5',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              flexWrap: 'wrap',
              gap: '1rem',
            }}
          >
            <div>
              <strong> Falha de Conexão: </strong>
              <span>{error}</span>
            </div>
            <button className="btn btn-secondary" onClick={loadData}>
              Tentar Reconectar
            </button>
          </div>
        )}

        {/* Botão de ajuda caso não haja nenhum dado carregado */}
        {apiOnline && filmes.length === 0 && salas.length === 0 && (
          <div
            style={{
              padding: '1.5rem',
              marginBottom: '2rem',
              background: 'linear-gradient(135deg, rgba(249, 115, 22, 0.15), rgba(139, 92, 246, 0.15))',
              border: '1px solid var(--border-glow)',
              borderRadius: 'var(--radius-md)',
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              flexWrap: 'wrap',
              gap: '1rem',
            }}
          >
            <div>
              <h4 style={{ fontSize: '1.1rem', marginBottom: '0.25rem' }}> Banco de Dados Inicial Limpo</h4>
              <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>
                Deseja popular dados reais de demonstração (filmes com cartazes, salas IMAX/3D/2D, tipos de ingresso e sessões) via REST API?
              </p>
            </div>
            <button
              className="btn btn-primary"
              onClick={handleSeedDemoData}
              disabled={seeding}
            >
              {seeding ? 'Populando...' : 'Inserir Dados de Demonstração'}
            </button>
          </div>
        )}

        {activeTab === 'filmes' && (
          <FilmesView
            filmes={filmes}
            loading={loading}
            onRefresh={loadData}
          />
        )}

        {activeTab === 'sessoes' && (
          <SessoesView
            sessoes={sessoes}
            filmes={filmes}
            salas={salas}
            loading={loading}
            onRefresh={loadData}
          />
        )}

        {activeTab === 'salas' && (
          <SalasView
            salas={salas}
            loading={loading}
            onRefresh={loadData}
          />
        )}

        {activeTab === 'ingressos' && (
          <IngressosView
            tiposIngresso={tiposIngresso}
            loading={loading}
            onRefresh={loadData}
          />
        )}
      </main>

      <footer className="footer">
        <p>PCS3643 - Laboratório de Engenharia de Software I | Sistema de Cinema & Ingressos (MVC + REST API)</p>
      </footer>
    </div>
  );
}
