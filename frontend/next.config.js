/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  transpilePackages: ['three', 'react-globe.gl'],
  images: { unoptimized: true },
};
module.exports = nextConfig;
