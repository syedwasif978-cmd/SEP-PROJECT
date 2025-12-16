// Accounts/Payments page helpers
console.log('account.js loaded');

// Error handler for account operations
function handleAccountError(error) {
  console.error('Account operation error:', error);
  try{ showToast('Account operation failed. Check console for details.', 'error'); }catch(e){console.error(e)}
}
