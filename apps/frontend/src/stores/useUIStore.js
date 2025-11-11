import { create } from 'zustand';
import { persist } from 'zustand/middleware';

/**
 * Unified UI store for theme and sidebar state.
 * Merged from useUIStore and useThemeStore to eliminate duplication.
 */
const useUIStore = create(
  persist(
    (set, get) => ({
      // Theme state
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

      // Sidebar state
      sidebarCollapsed: false,
      toggleSidebar: () => set((state) => ({ sidebarCollapsed: !state.sidebarCollapsed })),
      setSidebarCollapsed: (collapsed) => set({ sidebarCollapsed: collapsed }),
    }),
    {
      name: 'ui-storage',
      // Only persist theme and sidebar state
      partialize: (state) => ({ theme: state.theme, sidebarCollapsed: state.sidebarCollapsed }),
    }
  )
);

// Initialize theme on app start
export const initializeTheme = () => {
  const { theme, setTheme } = useUIStore.getState();
  setTheme(theme);
};

export default useUIStore;
