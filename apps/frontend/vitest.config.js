import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react'; // SWC for faster test transpilation
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
    setupFiles: './src/tests/setup.js',


    // M3 Max parallel testing optimization
    pool: 'threads',
    poolOptions: {
      threads: {
        maxThreads: 16, // Match M3 Max cores
        minThreads: 8,
      },
    },
    isolate: true, // Prevent test pollution

    // Coverage configuration
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html', 'lcov'],
      exclude: [
        'node_modules/',
        'src/tests/',
        '**/*.spec.{js,jsx}',
        '**/*.test.{js,jsx}',
        '**/dist/**',
      ],
      lines: 70,
      functions: 70,
      branches: 70,
      statements: 70,
    },

    // Better test output
    reporters: ['verbose', 'html'],
    outputFile: {
      html: './coverage/index.html',
    },
  },
});
