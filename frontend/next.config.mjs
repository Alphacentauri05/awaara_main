/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    remotePatterns: [
      {
        // Allow images from Cloudinary and any other CDN because you'll inevitably use random domains
        protocol: 'https',
        hostname: '**',
      },
    ],
  },
};

export default nextConfig;
