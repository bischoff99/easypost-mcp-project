"""Tracking and notification prompts."""


def register_tracking_prompts(mcp):
    """Register tracking-related prompts."""

    @mcp.prompt()
    def track_and_notify(tracking_number: str, recipient_email: str = None) -> str:
        """Track a shipment and format notification message."""
        email_part = (
            f" and prepare an email notification for {recipient_email}" if recipient_email else ""
        )
        return f"""Track shipment {tracking_number}{email_part}.

Please:
1. Use get_tracking tool to fetch current tracking status
2. Extract key information:
   - Current status
   - Current location
   - Estimated delivery date
   - Last update timestamp
3. Format the information in a clear, customer-friendly way{'''
4. Draft an email notification with:
   - Subject line
   - Body with tracking details
   - Next steps for recipient''' if recipient_email else ''}"""
