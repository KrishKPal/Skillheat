import { useNews, timeAgo } from '@/lib/api';
import type { NewsArticle } from '@/types/api';
import { useState } from 'react';

interface NewsStackProps {
  countryCode: string | null;
}

export function NewsStack({ countryCode }: NewsStackProps) {
  const { data: articles, error, isLoading } = useNews(countryCode, 100);

  return (
    <div
      style={{
        background: 'var(--bg-panel-deep)',
        border: '1px solid var(--border-subtle)',
        borderRadius: 'var(--radius-md)',
        padding: 12,
        flex: 1,
        minHeight: 0,
        display: 'flex',
        flexDirection: 'column',
      }}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 10, flexShrink: 0 }}>
        <span className="label-mono">
          NEWS · {countryCode ? countryCode : 'GLOBAL'}
        </span>
        {articles && articles.length > 0 && (
          <span style={{ fontFamily: 'var(--font-mono)', fontSize: 9, color: 'var(--live)', letterSpacing: 1 }}>
            ● {articles.length} LOADED
          </span>
        )}
      </div>

      <div style={{ overflowY: 'auto', flex: 1, display: 'flex', flexDirection: 'column', gap: 4 }}>
        {error && (
          <div style={{ color: 'var(--decline)', fontSize: 12, padding: 8 }}>
            Failed to load news. Is the backend running?
          </div>
        )}
        {isLoading && !articles && (
          <div className="label-mono" style={{ padding: 8 }}>LOADING…</div>
        )}
        {articles && articles.length === 0 && (
          <div className="label-mono" style={{ padding: 8 }}>
            {countryCode ? 'NO ARTICLES FOR THIS COUNTRY' : 'NO ARTICLES YET — RUN fetch_news'}


          </div>
        )}
        {articles && articles.map((article) => (
          <NewsItem key={article.id} article={article} />
        ))}
      </div>
    </div>
  );
}

function NewsItem({ article }: { article: NewsArticle }) {
  const [hovered, setHovered] = useState(false);

  // Color the left border by source category
  const tierColor =
    article.source.category === 'mainstream' ? 'var(--hot)' :
    article.source.category === 'funding' ? 'var(--warm)' :
    article.source.category === 'developer' ? 'var(--cool)' :
    'rgba(255,255,255,0.2)';

  // mock:// URLs are seeded fake URLs — they don't link anywhere
  const isMockUrl = article.url.startsWith('mock://');

  // Render as a real <a> so middle-click, Cmd+click, "Open in new tab" all work
  // We use display:block so the whole row is the click target
  const Wrapper = isMockUrl ? 'div' : 'a';
  const wrapperProps = isMockUrl
    ? {}
    : {
        href: article.url,
        target: '_blank',
        rel: 'noopener noreferrer',
      };

  return (
    <Wrapper
      {...wrapperProps}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      style={{
        display: 'block',
        borderLeft: `2px solid ${tierColor}`,
        padding: '6px 0 6px 10px',
        cursor: isMockUrl ? 'default' : 'pointer',
        background: hovered && !isMockUrl ? 'var(--bg-hover)' : 'transparent',
        textDecoration: 'none',
        color: 'inherit',
        transition: 'background 0.15s ease',
      }}
    >
      <div
        style={{
          fontSize: 12,
          color: 'var(--text-primary)',
          lineHeight: 1.35,
          // Subtle underline on hover so it's visually clear it's a link
          textDecoration: hovered && !isMockUrl ? 'underline' : 'none',
          textUnderlineOffset: 2,
          textDecorationColor: 'rgba(255,255,255,0.3)',
        }}
      >
        {article.title}
      </div>
      <div className="label-mono" style={{ marginTop: 3, display: 'flex', gap: 6, alignItems: 'center' }}>
        <span>{article.source.name.toUpperCase()}</span>
        <span style={{ color: 'var(--text-quaternary)' }}>·</span>
        <span>{timeAgo(article.published_at)}</span>
        {article.country_code && (
          <>
            <span style={{ color: 'var(--text-quaternary)' }}>·</span>
            <span>{article.country_code}</span>
          </>
        )}
        {isMockUrl && (
          <>
            <span style={{ color: 'var(--text-quaternary)' }}>·</span>
            <span style={{ color: 'var(--warm)' }}>MOCK</span>
          </>
        )}
      </div>
    </Wrapper>
  );
}
