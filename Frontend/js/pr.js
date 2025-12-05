// PR (Purchase Requisition) page helpers
console.log('pr.js loaded');

// Global function to handle errors in PR operations
function handleError(error, context = 'PR Operation') {
  console.error(`${context} error:`, error);
  alert(`Error: ${error.message || error}`);
}
