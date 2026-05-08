import { useNews, timeAgo } from '@/lib/api';
import type { NewsArticle } from '@/types/api';

export function TickerBar() {
  const { data: articles } = useNews(null, 12);

  if (!articles || articles.length === 0) {
    return (
      <div
        style={{
          padding: '6px 12px',
          background: 'var(--bg-panel-deep)',
          border: '1px solid var(--border-subtle)',
          borderRadius: 'var(--radius-md)',
          flexShrink: 0,
        }}
      >
        <span className="label-mono">LOADING TICKER</span>
      </div>
    );
  }

  return (
    <div
      style={{
        padding: '6px 0',
        background: 'var(--bg-panel-deep)',
        border: '1px solid var(--border-subtle)',
        borderRadius: 'var(--radius-md)',
        flexShrink: 0,
        overflow: 'hidden',
        whiteSpace: 'nowrap',
        position: 'relative',
      }}
    >
      <div
        className="ticker-track"
        style={{
          display: 'inline-flex',
          gap: 32,
          paddingLeft: 16,
          animation: 'ticker-scroll 90s linear infinite',
        }}
      >
        {[...articles, ...articles].map((article, i) => (
          <TickerItem key={`${article.id}-${i}`} article={article} />
        ))}
      </div>
    </div>
  );
}

function TickerItem({ article }: { article: NewsArticle }) {
  const color =
    article.source.category === 'ai' ? 'var(--hot)' :
    article.source.category === 'startups' || article.source.category === 'vc' ? 'var(--warm)' :
    article.source.category === 'developer' ? 'var(--cool)' :
    'var(--text-secondary)';

  const truncated =
    article.title.length > 80 ? article.title.slice(0, 80) + '...' : article.title;

  return (
      <a
      href={article.url}
      target="_blank"
      rel="noopener noreferrer"
      style={{
        fontFamily: 'var(--font-mono)',
        fontSize: 11,
        textDecoration: 'none',
        display: 'inline-flex',
        gap: 8,
        alignItems: 'center',
      }}
      title={article.title}
    >
      <span style={{ color, textTransform: 'uppercase', letterSpacing: 1 }}>
        {article.source.name}
      </span>
      <span style={{ color: 'var(--text-quaternary)' }}>·</span>
      <span style={{ color: 'var(--text-primary)' }}>{truncated}</span>
      <span style={{ color: 'var(--text-quaternary)' }}>
        {timeAgo(article.published_at)}
      </span>
    </a>
  );
}