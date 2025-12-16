// Negotiation page helpers
console.log('negotiation.js loaded');

// Error handler for negotiation operations
function handleNegotiationError(error) {
  console.error('Negotiation error:', error);
  try{ showToast('Negotiation operation failed. Check console for details.', 'error'); }catch(e){console.error(e)}
}
