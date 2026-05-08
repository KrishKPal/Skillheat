import Head from 'next/head';
import { useState } from 'react';
import { useGlobeState } from '@/lib/api';
import type { Country } from '@/types/api';
import { TopBar } from '@/components/TopBar';
import { GlobeView } from '@/components/Globe';
import { CountryHeader } from '@/components/CountryHeader';
import { NewsStack } from '@/components/NewsStack';
import { TickerBar } from '@/components/TickerBar';

export default function HomePage() {
  const [selectedCountry, setSelectedCountry] = useState<Country | null>(null);
  const { data: globe, error, isLoading } = useGlobeState();

  return (
    <>
      <Head>
        <title>SkillHeat — Global Tech Pulse</title>
      </Head>
      <div style={{ display: 'flex', flexDirection: 'column', height: '100vh', width: '100vw' }}>
        <TopBar
          selectedCountry={selectedCountry}
          onClearSelection={() => setSelectedCountry(null)}
        />

        {error && (
          <div style={{ padding: 16, color: 'var(--decline)' }}>
            Failed to load globe data. Is the backend running on http://localhost:8000?
          </div>
        )}

        {isLoading && (
          <div style={{ padding: 16 }} className="label-mono">LOADING GLOBE…</div>
        )}

        {globe && (
          <>
            <div
              style={{
                display: 'grid',
                gridTemplateColumns: 'minmax(0, 1.4fr) minmax(0, 1fr)',
                gap: 12,
                padding: 12,
                flex: 1,
                minHeight: 0,
              }}
            >
              <div
                style={{
                  background: 'var(--bg-panel-deep)',
                  border: '1px solid var(--border-subtle)',
                  borderRadius: 'var(--radius-md)',
                  overflow: 'hidden',
                }}
              >
                <GlobeView
                  countries={globe.countries}
                  selectedCode={selectedCountry?.code ?? null}
                  onSelectCountry={(c) => setSelectedCountry(c)}
                />
              </div>

              <div style={{ display: 'flex', flexDirection: 'column', gap: 8, minHeight: 0 }}>
                <CountryHeader
                  country={selectedCountry}
                  totalArticles24h={globe.total_articles_24h}
                />
                <NewsStack countryCode={selectedCountry?.code ?? null} />
              </div>
            </div>

            <div style={{ padding: '0 12px 12px' }}>
              <TickerBar />
            </div>
          </>
        )}
      </div>
    </>
  );
}
