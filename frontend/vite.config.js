import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react-swc'; // SWC for 5-20x faster transpilation on Apple Silicon
import path from 'path';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  // M3 Max optimizations
  build: {
    // Leverage M3 Max cores for builds
    rollupOptions: {
      maxParallelFileOps: 20, // Default is 20, M3 Max can handle more
      output: {
        manualChunks: {
          // Vendor chunks for better caching
          'vendor-react': ['react', 'react-dom', 'react-router-dom'],
          'vendor-charts': ['recharts'],
          'vendor-animation': ['framer-motion'],
          'vendor-ui': [
            '@radix-ui/react-dialog',
            '@radix-ui/react-dropdown-menu',
            '@radix-ui/react-popover',
            '@radix-ui/react-select',
            '@radix-ui/react-separator',
            '@radix-ui/react-slot',
            '@radix-ui/react-tabs',
          ],
          'vendor-forms': ['react-hook-form', 'zod'],
          'vendor-data': ['@tanstack/react-query', '@tanstack/react-table', 'zustand', 'immer'],
        },
      },
    },
    target: 'esnext', // Modern JS for M3 Safari
    minify: 'esbuild', // Faster than Terser, uses Go (parallelized)
    sourcemap: false, // Faster builds in dev
    chunkSizeWarningLimit: 600,
  },
  // Faster dev server for M3 Max
  server: {
    port: 5173,
    hmr: {
      overlay: true,
    },
    watch: {
      usePolling: false, // macOS native file watching
      interval: 100, // Faster detection
    },
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
  // Optimize deps resolution
  optimizeDeps: {
    esbuildOptions: {
      target: 'esnext',
      platform: 'browser',
    },
  },
});
