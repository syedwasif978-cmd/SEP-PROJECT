// Tax Calculator page helpers
console.log('tax.js loaded');

// Error handler for tax operations
function handleTaxError(error) {
  console.error('Tax calculation error:', error);
  try{ showToast('Tax calculation failed. Check console for details.', 'error'); }catch(e){console.error(e)}
}
