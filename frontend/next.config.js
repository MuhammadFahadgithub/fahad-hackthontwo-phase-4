// frontend/next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  webpack: (config, { isServer }) => {
    // Fix for node:crypto
    if (!isServer) {
      config.resolve.fallback = {
        ...config.resolve.fallback,
        crypto: false,
        stream: false,
        buffer: false,
      };
    }
    return config;
  },
  // Add this if using Better Auth
  experimental: {
    serverComponentsExternalPackages: ['better-auth'],
  },
};

module.exports = nextConfig;