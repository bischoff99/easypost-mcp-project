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


    // Parallel testing with auto-detected workers
    pool: 'threads',
    poolOptions: {
      threads: {
        singleThread: false,
      },
    },
    isolate: true,

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
