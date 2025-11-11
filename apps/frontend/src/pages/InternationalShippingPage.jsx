import ErrorBoundary from '@/components/ui/ErrorBoundary';
import InternationalShippingForm from '@/components/international/InternationalShippingForm';

/**
 * InternationalShippingPage
 *
 * Page for creating international shipments
 */
function InternationalShippingPageContent() {
  return <InternationalShippingForm />;
}

export default function InternationalShippingPage() {
  return (
    <ErrorBoundary>
      <InternationalShippingPageContent />
    </ErrorBoundary>
  );
}
