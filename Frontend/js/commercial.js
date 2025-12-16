// Commercial Approval page helpers
console.log('commercial.js loaded');

// Error handler for commercial operations
function handleCommercialError(error) {
  console.error('Commercial operation error:', error);
  try{ showToast('Commercial operation failed. Check console for details.', 'error'); }catch(e){console.error(e)}
}
