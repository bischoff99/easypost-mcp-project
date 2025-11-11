import { create } from 'zustand';
import { persist } from 'zustand/middleware';

/**
 * Notifications store
 * Manages notification state and unread count
 */
export const useNotificationsStore = create(
  persist(
    (set, get) => ({
      notifications: [],
      unreadCount: 0,

      addNotification: (notification) => {
        const notifications = get().notifications;
        set({
          notifications: [notification, ...notifications].slice(0, 50), // Keep last 50
          unreadCount: get().unreadCount + 1,
        });
      },

      markAsRead: (id) => {
        const notifications = get().notifications.map((n) =>
          n.id === id ? { ...n, read: true } : n
        );
        const unreadCount = notifications.filter((n) => !n.read).length;
        set({ notifications, unreadCount });
      },

      markAllAsRead: () => {
        const notifications = get().notifications.map((n) => ({ ...n, read: true }));
        set({ notifications, unreadCount: 0 });
      },

      clearNotifications: () => {
        set({ notifications: [], unreadCount: 0 });
      },

      setNotifications: (notifications) => {
        const unreadCount = notifications.filter((n) => !n.read).length;
        set({ notifications, unreadCount });
      },
    }),
    {
      name: 'notifications-storage',
    }
  )
);
