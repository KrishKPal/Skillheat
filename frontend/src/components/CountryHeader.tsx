import type { Country } from '@/types/api';

interface CountryHeaderProps {
  country: Country | null;
  totalArticles24h: number;
}

export function CountryHeader({ country, totalArticles24h }: CountryHeaderProps) {
  if (!country) {
    return (
      <div
        style={{
          background: 'var(--bg-panel-deep)',
          border: '1px solid var(--border-subtle)',
          borderRadius: 'var(--radius-md)',
          padding: 12,
          flexShrink: 0,
        }}
      >
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline' }}>
          <div>
            <div style={{ fontSize: 14, color: 'var(--text-primary)', fontWeight: 500 }}>Global Feed</div>
            <div className="label-mono" style={{ marginTop: 2 }}>ALL COUNTRIES · LAST 24H</div>
          </div>
          <div style={{ textAlign: 'right' }}>
            <div style={{ fontSize: 22, color: 'var(--warm)', fontWeight: 500, fontFamily: 'var(--font-mono)', lineHeight: 1 }}>
              {totalArticles24h}
            </div>
            <div className="label-mono" style={{ color: 'var(--warm)', marginTop: 2 }}>ARTICLES</div>
          </div>
        </div>
      </div>
    );
  }

  const heatLabel = country.heat_score >= 75 ? 'HOT' : country.heat_score >= 50 ? 'WARM' : country.heat_score >= 25 ? 'MID' : 'COOL';
  const heatColor = country.heat_score >= 75 ? 'var(--hot)' : country.heat_score >= 50 ? 'var(--warm)' : country.heat_score >= 25 ? 'var(--mid)' : 'var(--cool)';

  return (
    <div
      style={{
        background: 'var(--bg-panel-deep)',
        border: '1px solid var(--border-subtle)',
        borderRadius: 'var(--radius-md)',
        padding: 12,
        flexShrink: 0,
      }}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline' }}>
        <div>
          <div style={{ fontSize: 14, color: 'var(--text-primary)', fontWeight: 500 }}>{country.name}</div>
          <div className="label-mono" style={{ marginTop: 2 }}>
            {country.code} · {country.article_count_24h} ARTICLES · 24H
          </div>
        </div>
        <div style={{ textAlign: 'right' }}>
          <div style={{ fontSize: 22, color: heatColor, fontWeight: 500, fontFamily: 'var(--font-mono)', lineHeight: 1 }}>
            {Math.round(country.heat_score)}
          </div>
          <div className="label-mono" style={{ color: heatColor, marginTop: 2 }}>{heatLabel}</div>
        </div>
      </div>
    </div>
  );
}
