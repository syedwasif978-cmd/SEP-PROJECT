// Dashboard page: display API health status and basic info
console.log('dashboard.js loaded');

async function loadDashboard() {
  const statsDiv = document.getElementById('stats');
  if (!statsDiv) return;

  try {
    const [healthRes, infoRes] = await Promise.all([
      fetch('/api/health'),
      fetch('/api/info')
    ]);

    const health = healthRes.ok ? await healthRes.json() : {status: 'unknown'};
    const info = infoRes.ok ? await infoRes.json() : {app: 'SEP-PROJECT', version: 'n/a'};

    statsDiv.innerHTML = `
      <div class="card">
        <h3>System Status</h3>
        <p class="muted">Live health check</p>
        <div style="margin-top:12px">
          <span class="status-badge">${health.status || 'unknown'}</span>
        </div>
      </div>

      <div class="card">
        <h3>Service</h3>
        <p class="muted">Backend service name</p>
        <p style="margin-top:10px;font-weight:600">${health.service || info.app}</p>
      </div>

      <div class="card">
        <h3>Version</h3>
        <p class="muted">Application version</p>
        <p style="margin-top:10px;font-weight:600">${info.version || '1.0'}</p>
      </div>

      <div class="card">
        <h3>Raw Info</h3>
        <p class="muted">Quick JSON dump</p>
        <pre class="jsondump">${JSON.stringify({health, info}, null, 2)}</pre>
      </div>
    `;
  } catch (error) {
    console.error('Error loading dashboard:', error);
    statsDiv.innerHTML = '<div class="card"><p style="color: #ffb4b4;">Error loading dashboard. Backend may not be running.</p></div>';
  }
}

// Call on page load
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', loadDashboard);
} else {
  loadDashboard();
}
