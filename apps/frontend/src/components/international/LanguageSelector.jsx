import { useTranslation } from 'react-i18next'
import * as Select from '@radix-ui/react-select'
import { Check, ChevronDown, Languages } from 'lucide-react'
import { Button } from '@/components/ui/Button'

/**
 * LanguageSelector Component
 *
 * Dropdown for selecting UI language
 */
export default function LanguageSelector() {
  const { i18n } = useTranslation()

  const languages = [
    { code: 'en', name: 'English', flag: '🇺🇸' },
    { code: 'es', name: 'Español', flag: '🇪🇸' },
    { code: 'fr', name: 'Français', flag: '🇫🇷' },
    { code: 'de', name: 'Deutsch', flag: '🇩🇪' },
  ]

  const currentLanguage = languages.find((lang) => lang.code === i18n.language) || languages[0]

  const changeLanguage = (code) => {
    i18n.changeLanguage(code)
    localStorage.setItem('preferred-language', code)
  }

  return (
    <Select.Root value={i18n.language} onValueChange={changeLanguage}>
      <Select.Trigger asChild>
        <Button variant="ghost" size="sm" className="gap-2" aria-label="Select language">
          <Languages className="h-4 w-4" />
          <span className="hidden sm:inline">{currentLanguage.name}</span>
          <ChevronDown className="h-3 w-3 opacity-50" />
        </Button>
      </Select.Trigger>

      <Select.Portal>
        <Select.Content
          className="overflow-hidden rounded-md border bg-background shadow-lg z-50"
          position="popper"
          sideOffset={5}
        >
          <Select.Viewport className="p-1">
            {languages.map((lang) => (
              <Select.Item
                key={lang.code}
                value={lang.code}
                className="relative flex items-center gap-2 px-3 py-2 text-sm outline-none cursor-pointer hover:bg-accent rounded-sm data-[highlighted]:bg-accent"
              >
                <span className="text-base">{lang.flag}</span>
                <Select.ItemText>{lang.name}</Select.ItemText>
                {i18n.language === lang.code && (
                  <Select.ItemIndicator className="ml-auto">
                    <Check className="h-4 w-4" />
                  </Select.ItemIndicator>
                )}
              </Select.Item>
            ))}
          </Select.Viewport>
        </Select.Content>
      </Select.Portal>
    </Select.Root>
  )
}
