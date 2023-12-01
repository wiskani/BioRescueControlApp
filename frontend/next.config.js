/** @type {import('next').NextConfig} */
const nextConfig = {
    reactStrictMode: true,
    swcMinify: true,
    experimental: {
      appDir: true,
    },
        images: {
                remotePatterns: [
                        {
                                protocol: 'http',
                                hostname: 'localhost',
                        }
                ],
        },
  };

module.exports = nextConfig
