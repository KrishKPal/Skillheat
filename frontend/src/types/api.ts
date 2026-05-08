// TypeScript types matching the backend API exactly.
// Edit here when the backend schema changes.

export interface Country {
  code: string;
  name: string;
  latitude: number;
  longitude: number;
  heat_score: number;
  article_count_24h: number;
}

export interface NewsSource {
  slug: string;
  name: string;
  homepage_url: string | null;
  category: string;
}

export interface NewsArticle {
  id: number;
  title: string;
  summary: string | null;
  url: string;
  country_code: string | null;
  published_at: string;
  source: NewsSource;
}

export interface GlobeState {
  countries: Country[];
  total_articles_24h: number;
  last_updated: string;
}

export interface Health {
  status: string;
  database: string;
}

// GeoJSON country feature shape (a slice of the GeoJSON spec we actually use)
export interface CountryFeature {
  type: 'Feature';
  properties: {
    ISO_A2?: string;
    ADMIN?: string;
    name?: string;
  };
  geometry: object;
}

export interface CountryGeoJSON {
  type: 'FeatureCollection';
  features: CountryFeature[];
}
