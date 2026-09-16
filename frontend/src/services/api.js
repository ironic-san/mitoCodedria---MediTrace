const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || "http://localhost:8000").replace(/\/$/, "")

export class ApiError extends Error {
  constructor(status, message, payload) {
    super(message)
    this.status = status
    this.payload = payload
  }
}

const sessionKey = "meditrace.session"

export const session = {
  get: () => {
    try { return JSON.parse(sessionStorage.getItem(sessionKey) || "null") }
    catch { sessionStorage.removeItem(sessionKey); return null }
  },
  set: (value) => sessionStorage.setItem(sessionKey, JSON.stringify(value)),
  clear: () => sessionStorage.removeItem(sessionKey),
}

async function request(path, options = {}) {
  const activeSession = session.get()
  const headers = new Headers(options.headers || {})
  if (activeSession?.access_token) headers.set("Authorization", `Bearer ${activeSession.access_token}`)
  if (options.body && !(options.body instanceof FormData) && !headers.has("Content-Type")) {
    headers.set("Content-Type", "application/json")
  }

  let response
  try {
    response = await fetch(`${API_BASE_URL}${path}`, { ...options, headers })
  } catch {
    throw new ApiError(0, "Unable to reach MediTrace. Please check that the backend is running.")
  }
  const payload = await response.json().catch(() => null)
  if (!response.ok) {
    if (response.status === 401) {
      session.clear()
      if (typeof window !== "undefined" && window.location.pathname !== "/login") window.location.assign("/login")
    }
    throw new ApiError(response.status, payload?.detail || "The request could not be completed.", payload)
  }
  return payload
}

export const api = {
  login: (email, password) => request("/auth/login", { method: "POST", body: JSON.stringify({ email, password }) }),
  me: () => request("/auth/me"),
  patientMe: () => request("/patients/me"),
  patient: (id) => request(`/patients/${id}`),
  patientSummary: (id) => request(`/patients/${id}/medical-summary`),
  patientAudit: (id, query = "") => request(`/patients/${id}/audit${query}`),
  myAudit: () => request("/patients/me/audit-logs"),
  doctorMe: () => request("/doctors/me"),
  doctorPatients: () => request("/doctors/patients"),
  health: () => request("/health"),
  grantAccess: (patientId, payload) => request(`/patients/${patientId}/access`, { method: "POST", body: JSON.stringify(payload) }),
  revokeAccess: (patientId, accessId) => request(`/patients/${patientId}/access/${accessId}`, { method: "DELETE" }),
  uploadDocument: (form) => request("/documents/upload", { method: "POST", body: form }),
  document: (id) => request(`/documents/${id}`),
  documentAccess: (id) => request(`/documents/${id}/access`),
  ocr: (form) => request("/analysis/ocr", { method: "POST", body: form }),
  nlu: (payload) => request("/nlu/process", { method: "POST", body: JSON.stringify(payload) }),
  pipeline: (payload) => request("/analysis/pipeline", { method: "POST", body: JSON.stringify(payload) }),
  rag: (payload) => request("/analysis/rag", { method: "POST", body: JSON.stringify(payload) }),
  ragQuery: (payload) => request("/rag/query", { method: "POST", body: JSON.stringify(payload) }),
  ragDocuments: (patientId) => request(`/rag/patient/${patientId}/documents`),
  response: (payload) => request("/analysis/response", { method: "POST", body: JSON.stringify(payload) }),
  review: (payload) => request("/analysis/review", { method: "POST", body: JSON.stringify(payload) }),
  verifyIntegrity: (eventId) => request("/integrity/verify", { method: "POST", body: JSON.stringify({ event_id: eventId }) }),
  integrity: (eventId) => request(`/integrity/${eventId}`),
  breakGlass: (payload) => request("/emergency/break-glass", { method: "POST", body: JSON.stringify(payload) }),
  endBreakGlass: (payload) => request("/emergency/break-glass/end", { method: "POST", body: JSON.stringify(payload) }),
  emergencySummary: (patientId) => request(`/emergency/patient/${patientId}`),
  myEmergencySummary: () => request("/patients/me/emergency-summary"),
  genericAudit: (limit = 50, offset = 0) => request(`/audit/me?limit=${limit}&offset=${offset}`),
  patientAuditGeneric: (patientId, limit = 50, offset = 0) => request(`/audit/patient/${patientId}?limit=${limit}&offset=${offset}`),
}

export function readableError(error) {
  if (error?.status === 403) return "You do not have permission to perform this action."
  if (error?.status === 404) return "The requested record was not found."
  if (error?.status === 409) return "This record has changed already. Refresh and review the latest status."
  if (error?.status === 422) return "Please check the information entered and try again."
  if ([500, 502, 503].includes(error?.status)) return "The MediTrace backend could not complete processing. Please try again."
  return error?.message || "Something went wrong. Please try again."
}
