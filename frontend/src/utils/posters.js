/**
 * Mapeamento e geração de imagens de cartazes para os filmes.
 */

// Cartazes oficiais em alta definição para títulos conhecidos
const POSTER_DATABASE = {
  'duna': 'https://images.unsplash.com/photo-1534447677768-be436bb09401?q=80&w=600&auto=format&fit=crop',
  'duna: parte 2': 'https://images.unsplash.com/photo-1509198397868-475647b2a1e5?q=80&w=600&auto=format&fit=crop',
  'oppenheimer': 'https://images.unsplash.com/photo-1440404653325-ab127d49abc1?q=80&w=600&auto=format&fit=crop',
  'interestelar': 'https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=600&auto=format&fit=crop',
  'interstellar': 'https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=600&auto=format&fit=crop',
  'batman': 'https://images.unsplash.com/photo-1509281373149-e957c6296406?q=80&w=600&auto=format&fit=crop',
  'the batman': 'https://images.unsplash.com/photo-1509281373149-e957c6296406?q=80&w=600&auto=format&fit=crop',
  'avatar': 'https://images.unsplash.com/photo-1518709268805-4e9042af9f23?q=80&w=600&auto=format&fit=crop',
  'matrix': 'https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?q=80&w=600&auto=format&fit=crop',
  'blade runner': 'https://images.unsplash.com/photo-1508739773434-c26b3d09e071?q=80&w=600&auto=format&fit=crop',
  'star wars': 'https://images.unsplash.com/photo-1478760329108-5c3ed9d495a0?q=80&w=600&auto=format&fit=crop',
  'spider-man': 'https://images.unsplash.com/photo-1635805737707-575885ab0820?q=80&w=600&auto=format&fit=crop',
  'homem-aranha': 'https://images.unsplash.com/photo-1635805737707-575885ab0820?q=80&w=600&auto=format&fit=crop',
  'filme a': 'https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?q=80&w=600&auto=format&fit=crop',
  'filme b': 'https://images.unsplash.com/photo-1536440136628-849c177e76a1?q=80&w=600&auto=format&fit=crop',
};

const DEFAULT_POSTERS = [
  'https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?q=80&w=600&auto=format&fit=crop',
  'https://images.unsplash.com/photo-1536440136628-849c177e76a1?q=80&w=600&auto=format&fit=crop',
  'https://images.unsplash.com/photo-1478760329108-5c3ed9d495a0?q=80&w=600&auto=format&fit=crop',
  'https://images.unsplash.com/photo-1518709268805-4e9042af9f23?q=80&w=600&auto=format&fit=crop',
  'https://images.unsplash.com/photo-1440404653325-ab127d49abc1?q=80&w=600&auto=format&fit=crop',
];

/**
 * Gera um SVG elegante como poster de fallback caso a imagem remota não carregue
 */
export function getSvgPosterFallback(title = 'Cinema') {
  const safeTitle = (title || 'Cinema')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');

  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="400" height="600" viewBox="0 0 400 600">
    <defs>
      <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#1e1b4b" />
        <stop offset="50%" stop-color="#0f172a" />
        <stop offset="100%" stop-color="#31102b" />
      </linearGradient>
      <linearGradient id="glow" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#f97316" />
        <stop offset="100%" stop-color="#ef4444" />
      </linearGradient>
    </defs>
    <rect width="400" height="600" fill="url(#bg)" />
    <circle cx="200" cy="220" r="90" fill="none" stroke="url(#glow)" stroke-width="3" opacity="0.6" />
    <circle cx="200" cy="220" r="70" fill="none" stroke="#38bdf8" stroke-width="1.5" stroke-dasharray="8 6" opacity="0.4" />
    
    <!-- Film Reel Icon -->
    <path d="M175 195 L235 220 L175 245 Z" fill="url(#glow)" />
    
    <text x="200" y="380" font-family="Outfit, sans-serif" font-size="24" font-weight="bold" fill="#f8fafc" text-anchor="middle">
      ${safeTitle.length > 20 ? safeTitle.substring(0, 18) + '...' : safeTitle}
    </text>
    <text x="200" y="415" font-family="sans-serif" font-size="13" font-weight="600" fill="#f97316" text-anchor="middle" letter-spacing="3">
      CINEMA EM CARTAZ
    </text>
    <rect x="150" y="440" width="100" height="28" rx="14" fill="rgba(255,255,255,0.08)" stroke="rgba(255,255,255,0.15)" />
    <text x="200" y="458" font-family="sans-serif" font-size="11" font-weight="bold" fill="#94a3b8" text-anchor="middle">
      SALA DE CINEMA
    </text>
  </svg>`;

  return `data:image/svg+xml;utf8,${encodeURIComponent(svg)}`;
}

/**
 * Retorna o cartaz adequado para o filme pelo título ou código
 */
export function getMoviePoster(filme) {
  if (!filme) return getSvgPosterFallback();

  if (filme.cartaz_url) {
    return filme.cartaz_url;
  }

  const nameKey = (filme.nome || '').toLowerCase().trim();
  for (const [key, url] of Object.entries(POSTER_DATABASE)) {
    if (nameKey.includes(key)) {
      return url;
    }
  }

  // Se não encontrar por palavra-chave, usa hash determinístico do código/nome
  const index = Math.abs((filme.codigo || 0) + (filme.nome || '').length) % DEFAULT_POSTERS.length;
  return DEFAULT_POSTERS[index];
}
