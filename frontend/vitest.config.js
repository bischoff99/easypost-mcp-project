import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react-swc'; // SWC for faster test transpilation
import path from 'path';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: './src/test/setup.js',
    // M3 Max parallel testing optimization
    pool: 'threads',
    poolOptions: {
      threads: {
        maxThreads: 16, // Match M3 Max cores
        minThreads: 8,
      },
    },
    isolate: false, // Faster, shared context
  },
});
