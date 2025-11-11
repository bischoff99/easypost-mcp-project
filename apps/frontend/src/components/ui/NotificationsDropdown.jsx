import { Bell } from 'lucide-react';
import * as DropdownMenu from '@radix-ui/react-dropdown-menu';
import { Button } from '@/components/ui/Button';
import { Badge } from '@/components/ui/Badge';
import { useState, useEffect } from 'react';

/**
 * NotificationsDropdown Component
 *
 * Simplified notifications dropdown using local state instead of Zustand.
 * Notifications are ephemeral and don't need persistence.
 */
export default function NotificationsDropdown() {
  const [notifications, setNotifications] = useState([]);

  // Initialize with sample notifications if empty
  useEffect(() => {
    if (notifications.length === 0) {
      setNotifications([
        {
          id: '1',
          title: 'Shipment Created',
          message: 'Shipment shp_36ee98e957274becb05171608e28f3d9 has been created',
          type: 'success',
          read: false,
          createdAt: new Date().toISOString(),
        },
        {
          id: '2',
          title: 'Label Purchased',
          message: 'Label purchased for tracking number 9434636208303342135797',
          type: 'info',
          read: false,
          createdAt: new Date(Date.now() - 3600000).toISOString(),
        },
        {
          id: '3',
          title: 'Shipment In Transit',
          message: 'Your shipment is now in transit',
          type: 'info',
          read: false,
          createdAt: new Date(Date.now() - 7200000).toISOString(),
        },
      ]);
    }
  }, []);

  const unreadCount = notifications.filter((n) => !n.read).length;

  const markAsRead = (id) => {
    setNotifications((prev) =>
      prev.map((n) => (n.id === id ? { ...n, read: true } : n))
    );
  };

  const markAllAsRead = () => {
    setNotifications((prev) => prev.map((n) => ({ ...n, read: true })));
  };

  const clearNotifications = () => {
    setNotifications([]);
  };

  const getNotificationIcon = (type) => {
    switch (type) {
      case 'success':
        return '✓';
      case 'error':
        return '✕';
      case 'warning':
        return '⚠';
      default:
        return 'ℹ';
    }
  };

  const getNotificationColor = (type) => {
    switch (type) {
      case 'success':
        return 'text-green-600';
      case 'error':
        return 'text-red-600';
      case 'warning':
        return 'text-yellow-600';
      default:
        return 'text-blue-600';
    }
  };

  return (
    <DropdownMenu.Root>
      <DropdownMenu.Trigger asChild>
        <Button variant="ghost" size="icon" className="relative">
          <Bell className="h-5 w-5" />
          {unreadCount > 0 && (
            <Badge
              variant="destructive"
              className="absolute -top-1 -right-1 h-5 w-5 rounded-full p-0 text-xs flex items-center justify-center"
            >
              {unreadCount > 9 ? '9+' : unreadCount}
            </Badge>
          )}
          <span className="sr-only">Notifications</span>
        </Button>
      </DropdownMenu.Trigger>

      <DropdownMenu.Portal>
        <DropdownMenu.Content
          className="min-w-[320px] rounded-md border bg-background p-1 shadow-lg z-50"
          align="end"
          sideOffset={5}
        >
          <div className="px-3 py-2 border-b">
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-semibold">Notifications</h3>
              {unreadCount > 0 && (
                <Button
                  variant="ghost"
                  size="sm"
                  className="h-7 text-xs"
                  onClick={markAllAsRead}
                >
                  Mark all read
                </Button>
              )}
            </div>
          </div>

          <div className="max-h-[400px] overflow-y-auto">
            {notifications.length === 0 ? (
              <div className="px-3 py-8 text-center text-sm text-muted-foreground">
                No notifications
              </div>
            ) : (
              <div className="py-1">
                {notifications.slice(0, 10).map((notification) => (
                  <DropdownMenu.Item
                    key={notification.id}
                    className="flex items-start gap-3 px-3 py-2 rounded-sm hover:bg-accent cursor-pointer outline-none"
                    onClick={() => !notification.read && markAsRead(notification.id)}
                  >
                    <div
                      className={`mt-0.5 flex h-5 w-5 items-center justify-center rounded-full text-xs font-medium ${getNotificationColor(
                        notification.type
                      )}`}
                    >
                      {getNotificationIcon(notification.type)}
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-start justify-between gap-2">
                        <div className="flex-1">
                          <p
                            className={`text-sm font-medium ${
                              notification.read ? 'text-muted-foreground' : ''
                            }`}
                          >
                            {notification.title}
                          </p>
                          <p className="text-xs text-muted-foreground mt-1">
                            {notification.message}
                          </p>
                          <p className="text-xs text-muted-foreground mt-1">
                            {new Date(notification.createdAt).toLocaleString()}
                          </p>
                        </div>
                        {!notification.read && (
                          <div className="h-2 w-2 rounded-full bg-primary mt-1 flex-shrink-0" />
                        )}
                      </div>
                    </div>
                  </DropdownMenu.Item>
                ))}
              </div>
            )}
          </div>

          {notifications.length > 0 && (
            <div className="px-3 py-2 border-t">
              <Button
                variant="ghost"
                size="sm"
                className="w-full h-7 text-xs"
                onClick={clearNotifications}
              >
                Clear all
              </Button>
            </div>
          )}
        </DropdownMenu.Content>
      </DropdownMenu.Portal>
    </DropdownMenu.Root>
  );
}
