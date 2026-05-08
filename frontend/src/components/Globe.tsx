import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import dynamic from 'next/dynamic';
import type { Country, CountryGeoJSON, CountryFeature } from '@/types/api';

const Globe = dynamic(() => import('react-globe.gl'), { ssr: false });

interface GlobeViewProps {
  countries: Country[];
  selectedCode: string | null;
  onSelectCountry: (country: Country) => void;
}

// Stronger colors so heat data pops against the dark globe
function heatColor(score: number, alpha = 1): string {
  if (score >= 75) return `rgba(239, 68, 68, ${alpha})`;
  if (score >= 50) return `rgba(245, 158, 11, ${alpha})`;
  if (score >= 25) return `rgba(251, 191, 36, ${alpha})`;
  if (score > 0)   return `rgba(59, 130, 246, ${alpha})`;
  return `rgba(40, 60, 90, ${alpha})`; // dim baseline for countries with no data
}

function isoCode(feature: CountryFeature): string | undefined {
  return feature.properties.ISO_A2 || (feature.properties as { iso_a2?: string }).iso_a2;
}

export function GlobeView({ countries, selectedCode, onSelectCountry }: GlobeViewProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [size, setSize] = useState({ width: 600, height: 500 });
  const [geo, setGeo] = useState<CountryGeoJSON | null>(null);
  const [hoveredCode, setHoveredCode] = useState<string | null>(null);

  useEffect(() => {
    fetch('/countries.geojson')
      .then((r) => r.json())
      .then((data: CountryGeoJSON) => setGeo(data))
      .catch((e) => console.error('Failed to load country boundaries:', e));
  }, []);

  useEffect(() => {
    if (!containerRef.current) return;
    const el = containerRef.current;
    const ro = new ResizeObserver((entries) => {
      const { width, height } = entries[0].contentRect;
      setSize({ width: Math.floor(width), height: Math.floor(height) });
    });
    ro.observe(el);
    return () => ro.disconnect();
  }, []);

  const countryByCode = useMemo(() => {
    const map = new Map<string, Country>();
    for (const c of countries) map.set(c.code, c);
    return map;
  }, [countries]);

  // Significantly more visible polygon colors
  const polygonCapColor = useCallback(
    (feat: object) => {
      const f = feat as CountryFeature;
      const code = isoCode(f);
      if (!code) return 'rgba(40, 60, 90, 0.4)';
      const country = countryByCode.get(code);
      const score = country?.heat_score ?? 0;
      if (code === selectedCode) return heatColor(Math.max(score, 50), 0.95);
      if (code === hoveredCode)  return heatColor(Math.max(score, 35), 0.85);
      return heatColor(score, 0.7); // bumped from 0.55 — much more visible
    },
    [countryByCode, selectedCode, hoveredCode],
  );

  const polygonStrokeColor = useCallback(
    (feat: object) => {
      const f = feat as CountryFeature;
      return isoCode(f) === selectedCode
        ? 'rgba(255, 255, 255, 0.9)'
        : 'rgba(255, 255, 255, 0.25)'; // bumped from 0.15
    },
    [selectedCode],
  );

  // Higher altitudes = more visible 3D pop
  const polygonAltitude = useCallback(
    (feat: object) => {
      const f = feat as CountryFeature;
      const code = isoCode(f);
      if (code === selectedCode) return 0.025;
      if (code === hoveredCode)  return 0.018;
      return 0.01;
    },
    [selectedCode, hoveredCode],
  );

  const handlePolygonClick = useCallback(
    (feat: object) => {
      const f = feat as CountryFeature;
      const code = isoCode(f);
      if (!code) return;
      const country = countryByCode.get(code);
      if (country) {
        onSelectCountry(country);
      } else {
        onSelectCountry({
          code,
          name: f.properties.ADMIN || f.properties.name || code,
          latitude: 0,
          longitude: 0,
          heat_score: 0,
          article_count_24h: 0,
        });
      }
    },
    [countryByCode, onSelectCountry],
  );

  const polygonLabel = useCallback(
    (feat: object) => {
      const f = feat as CountryFeature;
      const code = isoCode(f);
      const country = code ? countryByCode.get(code) : undefined;
      const name = f.properties.ADMIN || f.properties.name || 'Unknown';
      const score = country ? Math.round(country.heat_score) : 0;
      const count = country?.article_count_24h ?? 0;
      return `<div style="background:#0a0e1a;border:1px solid rgba(255,255,255,0.15);padding:8px 12px;color:#e8e8e8;font-size:12px;border-radius:4px"><div style="font-weight:500">${name}</div><div style="font-family:ui-monospace;font-size:11px;color:#f59e0b;margin-top:2px">HEAT ${score} · ${count} ARTICLES</div></div>`;
    },
    [countryByCode],
  );

  const handleHover = useCallback((feat: object | null) => {
    if (!feat) { setHoveredCode(null); return; }
    const code = isoCode(feat as CountryFeature);
    setHoveredCode(code ?? null);
  }, []);

  return (
    <div
      ref={containerRef}
      style={{
        width: '100%',
        height: '100%',
        position: 'relative',
        background: 'radial-gradient(ellipse at center, #0a1828 0%, #050810 70%)',
        cursor: hoveredCode ? 'pointer' : 'grab',
      }}
    >
      <Globe
        width={size.width}
        height={size.height}
        backgroundColor="rgba(0,0,0,0)"
        // Switched from earth-night.jpg to a flat dark blue sphere — way faster
        // and lets the country heat colors stand out instead of competing with city lights
       globeImageUrl="//unpkg.com/three-globe/example/img/earth-blue-marble.jpg"
        showGlobe={true}
        showAtmosphere
        atmosphereColor="#3b82f6"
        atmosphereAltitude={0.15}
        polygonsData={geo?.features ?? []}
    polygonCapColor={() => 'rgba(0, 0, 0, 0)'}
    polygonSideColor={() => 'rgba(0, 0, 0, 0)'}
    polygonStrokeColor={polygonStrokeColor}
    polygonAltitude={0.005}
    polygonLabel={polygonLabel}
    onPolygonClick={handlePolygonClick}
    onPolygonHover={handleHover}
    pointsData={countries.filter(c => c.heat_score > 0)}
    pointLat="latitude"
    pointLng="longitude"
    pointColor={(d: object) => {
      const c = d as Country;
      if (c.code === selectedCode) return '#ffffff';
      if (c.heat_score >= 75) return '#ef4444';
      if (c.heat_score >= 50) return '#f59e0b';
      if (c.heat_score >= 25) return '#fbbf24';
      return '#3b82f6';
    }}
    pointAltitude={(d: object) => {
      const c = d as Country;
      return 0.01 + (c.heat_score / 100) * 0.04;
    }}
    pointRadius={(d: object) => {
      const c = d as Country;
      return 0.4 + (c.heat_score / 100) * 0.5;
    }}
    pointLabel={(d: object) => {
      const c = d as Country;
      return `<div style="background:#0a0e1a;border:1px solid rgba(255,255,255,0.15);padding:8px 12px;color:#e8e8e8;font-size:12px;border-radius:4px"><div style="font-weight:500">${c.name}</div><div style="font-family:ui-monospace;font-size:11px;color:#f59e0b;margin-top:2px">HEAT ${Math.round(c.heat_score)} · ${c.article_count_24h} ARTICLES</div></div>`;
    }}
    onPointClick={(d: object) => onSelectCountry(d as Country)}
      />
      <div
        style={{
          position: 'absolute', bottom: 12, left: 12,
          fontFamily: 'var(--font-mono)', fontSize: 10,
          color: 'var(--text-tertiary)', letterSpacing: 1, pointerEvents: 'none',
        }}
      >
        <div style={{ marginBottom: 4 }}>HEAT GRADIENT</div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
          <span style={{ width: 8, height: 8, background: '#3b82f6' }} />
          <span>COOL</span>
          <span style={{ width: 80, height: 4, background: 'linear-gradient(90deg, #3b82f6, #fbbf24, #f59e0b, #ef4444)' }} />
          <span style={{ width: 8, height: 8, background: '#ef4444' }} />
          <span>HOT</span>
        </div>
      </div>
      {!selectedCode && (
        <div
          style={{
            position: 'absolute', top: 12, right: 12,
            fontFamily: 'var(--font-mono)', fontSize: 10,
            color: 'var(--text-tertiary)', letterSpacing: 1, pointerEvents: 'none',
          }}
        >
          CLICK A COUNTRY ↗
        </div>
      )}
    </div>
  );
}
