const zafo = {
  apiKey: null,
  init: function(apiKey) {
    this.apiKey = apiKey;
    // Set up cookie (simplified - use a library for production)
    //...
  },
  trackEvent: function(eventType, eventData) {
    // Get user ID from cookie
    //...
    const event = {
      userId: userId,
      eventType: eventType,
      eventData: eventData,
      timestamp: Date.now()
    };
    // Send event to backend API
    fetch('/api/events', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': this.apiKey // Include API key for security
      },
      body: JSON.stringify(event)
    });
  }
};
// Example Event Tracking on Button Click
document.getElementById('myButton').addEventListener('click', () => {
  zafo.trackEvent('button_click', { buttonId: 'myButton' });
});
