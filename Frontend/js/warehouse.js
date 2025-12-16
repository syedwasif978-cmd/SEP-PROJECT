// Warehouse/PR page helpers
console.log('warehouse.js loaded');

// Error handler for warehouse operations
function handleWarehouseError(error) {
  console.error('Warehouse operation error:', error);
  try{ showToast('Warehouse operation failed. Check console for details.', 'error'); }catch(e){console.error(e)}
}
