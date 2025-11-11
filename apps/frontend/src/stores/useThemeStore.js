import { create } from 'zustand';
import { persist } from 'zustand/middleware';

// Theme store with persistence
export const useThemeStore = create(
  persist(
    (set, get) => ({
      theme: 'light',
      setTheme: (theme) => {
        set({ theme });
        // Update document class for Tailwind dark mode
        if (theme === 'dark') {
          document.documentElement.classList.add('dark');
        } else {
          document.documentElement.classList.remove('dark');
        }
      },
      toggleTheme: () => {
        const currentTheme = get().theme;
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        get().setTheme(newTheme);
      },
    }),
    {
      name: 'theme-storage', // Key for localStorage
      // Only persist the theme value
      partialize: (state) => ({ theme: state.theme }),
    }
  )
);

// Initialize theme on app start
export const initializeTheme = () => {
  const { theme, setTheme } = useThemeStore.getState();
  setTheme(theme);
};
