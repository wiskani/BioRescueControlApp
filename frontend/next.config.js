/** @type {import('next').NextConfig} */
const nextConfig = {
    reactStrictMode: true,
    swcMinify: true,
    experimental: {
      appDir: true,
    },
    output: 'standalone',
        //images: {
        //        remotePatterns: [
        //                {
        //                        protocol: 'http',
        //                        hostname: 'localhost',
        //                }
        //        ],
        //},
  };

module.exports = nextConfig
