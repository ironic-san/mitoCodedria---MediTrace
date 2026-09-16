export function LoadingState({ label = "Loading records…" }) {
  return <div className="dashboard-panel" role="status">{label}</div>
}

export function ErrorState({ error, onRetry }) {
  return <div className="dashboard-panel" role="alert"><strong>Unable to load records.</strong><p>{error}</p>{onRetry && <button type="button" className="secondary-action-button" onClick={onRetry}>Try again</button>}</div>
}

export function EmptyState({ label = "No records are available yet." }) {
  return <div className="dashboard-panel">{label}</div>
}
