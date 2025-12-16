// Vendors page helpers - error handling and utilities
console.log('vendors.js loaded');

// Error handler for vendor operations
function handleVendorError(error) {
  console.error('Vendor error:', error);
  try{ showToast('Vendor operation failed. Check console for details.', 'error'); }catch(e){console.error(e)}
}
