// Simple toast notifications
function showToast(message, type='info', timeout=4000){
  try{
    let container = document.getElementById('toast-container');
    if(!container){
      container = document.createElement('div');
      container.id = 'toast-container';
      document.body.appendChild(container);
    }
    const t = document.createElement('div');
    t.className = 'toast '+type;
    t.textContent = message;
    container.appendChild(t);
    // auto remove
    setTimeout(()=>{ t.classList.add('hide'); setTimeout(()=>t.remove(),300); }, timeout);
  }catch(e){ console.error('toast error', e); }
}

// expose for other scripts
window.showToast = showToast;
