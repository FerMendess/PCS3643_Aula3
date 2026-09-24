/**
 * Mapeamento e geração de imagens de cartazes para os filmes.
 */

// Cartazes oficiais reais de cinema (TMDB CDN em alta definição)
const POSTER_DATABASE = {
  // Filmes da base atual
  'oppenheimer': 'https://image.tmdb.org/t/p/w600_and_h900_bestv2/8Gxv8gSFCU0XGDykEGv7zR1n2ua.jpg',
  'past lives': 'https://image.tmdb.org/t/p/w600_and_h900_bestv2/k3waqVXSnvCZWfJYNtdamTgTtTA.jpg',
  'vidas passadas': 'https://image.tmdb.org/t/p/w600_and_h900_bestv2/k3waqVXSnvCZWfJYNtdamTgTtTA.jpg',
  'anatomy of a fall': 'https://image.tmdb.org/t/p/w600_and_h900_bestv2/kQs6keheMwCxJxrzVHY5xYsRbgK.jpg',
  'anatomia de uma queda': 'https://image.tmdb.org/t/p/w600_and_h900_bestv2/kQs6keheMwCxJxrzVHY5xYsRbgK.jpg',
  'the zone of interest': 'https://image.tmdb.org/t/p/w600_and_h900_bestv2/hUu9zyZmDD8VZAvQ2apEH1wwvRi.jpg',
  'zona de interesse': 'https://image.tmdb.org/t/p/w600_and_h900_bestv2/hUu9zyZmDD8VZAvQ2apEH1wwvRi.jpg',
  'anora': 'https://image.tmdb.org/t/p/w600_and_h900_bestv2/7MrVuqzgxIkm7yGkY8fB8yU8Zg7.jpg',
  'the brutalist': 'https://image.tmdb.org/t/p/w600_and_h900_bestv2/w2c9p24s5bU5oX6iF5K8V7yA6gO.jpg',
  'o brutalista': 'https://image.tmdb.org/t/p/w600_and_h900_bestv2/w2c9p24s5bU5oX6iF5K8V7yA6gO.jpg',
  'everything everywhere all at once': 'https://image.tmdb.org/t/p/w600_and_h900_bestv2/w3LxiVYPqrlexP02048TegqLFY4.jpg',
  'tudo em todo o lugar': 'https://image.tmdb.org/t/p/w600_and_h900_bestv2/w3LxiVYPqrlexP02048TegqLFY4.jpg',

  // Outros títulos populares
  'duna': 'https://image.tmdb.org/t/p/w600_and_h900_bestv2/czembW0Rk1Ke7lCJGahbOhdCuhV.jpg',
  'dune': 'https://image.tmdb.org/t/p/w600_and_h900_bestv2/czembW0Rk1Ke7lCJGahbOhdCuhV.jpg',
  'interestelar': 'https://image.tmdb.org/t/p/w600_and_h900_bestv2/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg',
  'interstellar': 'https://image.tmdb.org/t/p/w600_and_h900_bestv2/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg',
  'the batman': 'https://image.tmdb.org/t/p/w600_and_h900_bestv2/74xTEgt7R36Fpooo50r9T25onhq.jpg',
  'batman': 'https://image.tmdb.org/t/p/w600_and_h900_bestv2/74xTEgt7R36Fpooo50r9T25onhq.jpg',
  'avatar': 'https://image.tmdb.org/t/p/w600_and_h900_bestv2/kyeqWdyUXW608qlYkRqosgbbJyK.jpg',
  'matrix': 'https://image.tmdb.org/t/p/w600_and_h900_bestv2/f89U3ADr1oiB1s9GkdPOEpXUk5H.jpg',
  'spider-man': 'https://image.tmdb.org/t/p/w600_and_h900_bestv2/5weKu49GgC2Y19p5bS2zGg1rKek.jpg',
  'homem-aranha': 'https://image.tmdb.org/t/p/w600_and_h900_bestv2/5weKu49GgC2Y19p5bS2zGg1rKek.jpg',
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