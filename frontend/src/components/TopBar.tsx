import { useGlobeState, useHealth, useNews, timeAgo } from '@/lib/api';
import type { Country } from '@/types/api';
import { useMemo } from 'react';

interface TopBarProps {
  selectedCountry: Country | null;
  onClearSelection: () => void;
}

export function TopBar({ selectedCountry, onClearSelection }: TopBarProps) {
  const { data: globe } = useGlobeState();
  const { data: health } = useHealth();
  const { data: latestNews } = useNews(null, 5);
  const isLive = health?.status === 'ok' && health?.database === 'ok';

  // Find the hottest country right now — that's the actually interesting datapoint
  const hottest = useMemo(() => {
    if (!globe?.countries) return null;
    return [...globe.countries].sort((a, b) => b.heat_score - a.heat_score)[0];
  }, [globe]);

  const newest = latestNews?.[0];

  return (
      <header
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          padding: '10px 16px',
          borderBottom: '1px solid var(--border-subtle)',
          background: 'var(--bg-page)',
          flexShrink: 0,
          gap: 16,
        }}
      >

      <div style={{ display: 'flex', alignItems: 'center', gap: 20, minWidth: 0 }}>
        <span style={{ fontFamily: 'var(--font-mono)', fontSize: 13, letterSpacing: 2, color: 'var(--text-primary)' }}>
          SKILLHEAT
        </span>
        <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
          <span className="pulse-dot" style={{ background: isLive ? 'var(--live)' : 'var(--decline)' }} />
          <span style={{ fontFamily: 'var(--font-mono)', fontSize: 11, color: isLive ? 'var(--live)' : 'var(--decline)', letterSpacing: 1 }}>
            {isLive ? 'LIVE' : 'OFFLINE'}
          </span>
        </div>
        {selectedCountry ? (
          <button
            onClick={onClearSelection}
            style={{
              background: 'rgba(245, 158, 11, 0.1)',
              border: '1px solid var(--warm)',
              color: 'var(--warm)',
              padding: '3px 10px',
              fontFamily: 'var(--font-mono)',
              fontSize: 10,
              letterSpacing: 1,
              cursor: 'pointer',
              borderRadius: 'var(--radius-sm)',
            }}
          >
            {selectedCountry.code} · {selectedCountry.name.toUpperCase()} ✕
          </button>
        ) : (
          <span className="label-mono">GLOBAL</span>
        )}
      </div>

      {/* Middle: rotating signal — the most useful piece of info */}
      <div style={{ flex: 1, display: 'flex', justifyContent: 'center', minWidth: 0, overflow: 'hidden' }}>
        {newest && (
            <a
            href={newest.url}
            target="_blank"
            rel="noopener noreferrer"
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: 8,
              fontSize: 11,
              color: 'var(--text-secondary)',
              fontFamily: 'var(--font-mono)',
              textDecoration: 'none',
              maxWidth: '100%',
              overflow: 'hidden',
              whiteSpace: 'nowrap',
              textOverflow: 'ellipsis',
            }}
            title={newest.title}
          >
            <span style={{ color: 'var(--live)' }}>● BREAKING</span>
            <span style={{ overflow: 'hidden', textOverflow: 'ellipsis' }}>{newest.title}</span>
            <span style={{ color: 'var(--text-quaternary)' }}>{timeAgo(newest.published_at)}</span>
          </a>
        )}
      </div>

      {/* Right cluster: hottest country + counts */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 16, flexShrink: 0 }}>
        {hottest && (
          <span style={{ fontFamily: 'var(--font-mono)', fontSize: 11, color: 'var(--hot)' }}>
            ▲ HOTTEST {hottest.code} {Math.round(hottest.heat_score)}
          </span>
        )}
        {globe && (
          <span className="label-mono">{globe.total_articles_24h} ARTICLES · 24H</span>
        )}
      </div>
    </header>
  );
}
