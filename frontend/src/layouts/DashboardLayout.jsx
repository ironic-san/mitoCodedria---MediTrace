import { NavLink, Link } from "react-router-dom"

function Icon({ name }) {
  const common = {
    width: 18,
    height: 18,
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: "currentColor",
    strokeWidth: 1.8,
    strokeLinecap: "round",
    strokeLinejoin: "round",
    "aria-hidden": "true",
  }

  const icons = {
    dashboard: (
      <svg {...common}>
        <rect x="3" y="3" width="7" height="7" rx="1.5" />
        <rect x="14" y="3" width="7" height="7" rx="1.5" />
        <rect x="3" y="14" width="7" height="7" rx="1.5" />
        <rect x="14" y="14" width="7" height="7" rx="1.5" />
      </svg>
    ),

    patients: (
      <svg {...common}>
        <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2" />
        <circle cx="9" cy="7" r="4" />
        <path d="M22 21v-2a4 4 0 0 0-3-3.87" />
        <path d="M16 3.13a4 4 0 0 1 0 7.75" />
      </svg>
    ),

    passport: (
      <svg {...common}>
        <rect x="4" y="3" width="16" height="18" rx="2" />
        <circle cx="12" cy="9" r="3" />
        <path d="M8 16h8" />
        <path d="M9 19h6" />
      </svg>
    ),

    timeline: (
      <svg {...common}>
        <circle cx="12" cy="12" r="9" />
        <path d="M12 7v5l3 2" />
      </svg>
    ),

    documents: (
      <svg {...common}>
        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
        <path d="M14 2v6h6" />
        <path d="M8 13h8" />
        <path d="M8 17h6" />
      </svg>
    ),

    ai: (
      <svg {...common}>
        <path d="M12 3l1.5 5.5L19 10l-5.5 1.5L12 17l-1.5-5.5L5 10l5.5-1.5L12 3z" />
        <path d="M19 16l.7 2.3L22 19l-2.3.7L19 22l-.7-2.3L16 19l2.3-.7L19 16z" />
      </svg>
    ),

    integrity: (
      <svg {...common}>
        <path d="M12 3l7 3v5c0 4.5-3 8.2-7 10-4-1.8-7-5.5-7-10V6l7-3z" />
        <path d="M9 12l2 2 4-4" />
      </svg>
    ),

    emergency: (
      <svg {...common}>
        <path d="M12 3v18" />
        <path d="M3 12h18" />
        <path d="M7.5 7.5l9 9" />
        <path d="M16.5 7.5l-9 9" />
      </svg>
    ),

    audit: (
      <svg {...common}>
        <path d="M4 5h16" />
        <path d="M4 12h16" />
        <path d="M4 19h16" />
        <circle cx="8" cy="5" r="1" />
        <circle cx="15" cy="12" r="1" />
        <circle cx="10" cy="19" r="1" />
      </svg>
    ),

    settings: (
      <svg {...common}>
        <circle cx="12" cy="12" r="3" />
        <path d="M19.4 15a1.7 1.7 0 0 0 .34 1.88l.06.06-1.7 1.7-.06-.06a1.7 1.7 0 0 0-1.88-.34 1.7 1.7 0 0 0-1.03 1.55V20h-2.4v-.21a1.7 1.7 0 0 0-1.03-1.55 1.7 1.7 0 0 0-1.88.34l-.06.06-1.7-1.7.06-.06A1.7 1.7 0 0 0 8.4 15a1.7 1.7 0 0 0-1.55-1.03H6.6v-2.4h.25A1.7 1.7 0 0 0 8.4 10a1.7 1.7 0 0 0-.34-1.88L8 8.06l1.7-1.7.06.06a1.7 1.7 0 0 0 1.88.34A1.7 1.7 0 0 0 12.67 5.2V5h2.4v.2a1.7 1.7 0 0 0 1.03 1.56 1.7 1.7 0 0 0 1.88-.34l.06-.06 1.7 1.7-.06.06A1.7 1.7 0 0 0 19.4 10a1.7 1.7 0 0 0 1.55 1.03h.25v2.4h-.25A1.7 1.7 0 0 0 19.4 15z" />
      </svg>
    ),

    logout: (
      <svg {...common}>
        <path d="M10 17l5-5-5-5" />
        <path d="M15 12H3" />
        <path d="M13 5V3a1 1 0 0 1 1-1h6a1 1 0 0 1 1 1v18a1 1 0 0 1-1 1h-6a1 1 0 0 1-1-1v-2" />
      </svg>
    ),

    bell: (
      <svg
        width="18"
        height="18"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="1.8"
        strokeLinecap="round"
        strokeLinejoin="round"
        aria-hidden="true"
      >
        <path d="M18 8a6 6 0 0 0-12 0c0 7-3 7-3 9h18c0-2-3-2-3-9" />
        <path d="M10 21h4" />
      </svg>
    ),
  }

  return icons[name] || null
}

function DashboardLayout({
  children,
  role = "patient",
  userName = "Kabir Malhotra",
}) {
  const patientLinks = [
    {
      name: "Dashboard",
      path: "/patient/dashboard",
      icon: "dashboard",
    },
    {
      name: "Emergency Passport",
      path: "/patient/passport",
      icon: "passport",
    },
    {
      name: "Medical Timeline",
      path: "/patient/timeline",
      icon: "timeline",
    },
    {
      name: "Documents",
      path: "/patient/documents",
      icon: "documents",
    },
    {
      name: "Access Control",
      path: "/patient/access",
      icon: "integrity",
    },
    {
      name: "Access History",
      path: "/patient/access-history",
      icon: "audit",
    },
  ]

  const doctorLinks = [
    {
      name: "Dashboard",
      path: "/doctor/dashboard",
      icon: "dashboard",
    },
    {
      name: "Patients",
      path: "/doctor/patients",
      icon: "patients",
    },
    {
      name: "Emergency Passport",
      path: "/doctor/passport",
      icon: "passport",
    },
    {
      name: "Medical Timeline",
      path: "/doctor/timeline",
      icon: "timeline",
    },
    {
      name: "Documents",
      path: "/doctor/documents",
      icon: "documents",
    },
    {
      name: "AI Reviews",
      path: "/doctor/ai-reviews",
      icon: "ai",
    },
    {
      name: "Integrity",
      path: "/doctor/integrity",
      icon: "integrity",
    },
    {
      name: "Emergency",
      path: "/doctor/emergency",
      icon: "emergency",
    },
    {
      name: "Audit Trail",
      path: "/doctor/audit",
      icon: "audit",
    },
  ]

  const links = role === "doctor" ? doctorLinks : patientLinks

  const initials = userName
    .split(" ")
    .map((word) => word[0])
    .join("")
    .slice(0, 2)
    .toUpperCase()

  return (
    <div className="dashboard-layout">
      {/* =========================
          SIDEBAR
          ========================= */}

      <aside className="dashboard-sidebar">
        <Link to="/" className="dashboard-logo">
          Medi<span>-</span>Trace
        </Link>

        <div className="sidebar-subtitle">
          Emergency Health Platform
        </div>

        <nav className="sidebar-navigation">
          <div className="navigation-label">
            {role === "doctor" ? "CLINICAL" : "MY HEALTH"}
          </div>

          {links.map((link) => (
            <NavLink
              key={link.path}
              to={link.path}
              className={({ isActive }) =>
                `sidebar-link ${isActive ? "active" : ""}`
              }
            >
              <span className="sidebar-icon">
                <Icon name={link.icon} />
              </span>

              <span className="sidebar-link-text">
                {link.name}
              </span>
            </NavLink>
          ))}
        </nav>

        <div className="sidebar-bottom">
          <NavLink
            to={`/${role}/profile`}
            className={({ isActive }) =>
              `sidebar-link ${isActive ? "active" : ""}`
            }
          >
            <span className="sidebar-icon">
              <Icon name="settings" />
            </span>

            <span className="sidebar-link-text">
              Profile & Settings
            </span>
          </NavLink>

          <Link
            to="/"
            className="sidebar-link logout-link"
          >
            <span className="sidebar-icon">
              <Icon name="logout" />
            </span>

            <span className="sidebar-link-text">
              Logout
            </span>
          </Link>
        </div>
      </aside>

      {/* =========================
          MAIN AREA
          ========================= */}

      <div className="dashboard-main">
        <header className="dashboard-header">
          <div className="mobile-logo">
            <Link to="/">
              Medi<span>-</span>Trace
            </Link>
          </div>

          <div className="header-spacer"></div>

          {/* Emergency status */}
          <div className="header-emergency-status">
            <span className="status-dot"></span>
            <span>Emergency Ready</span>
          </div>

          {/* Notifications */}
          <button
            type="button"
            className="notification-button"
            aria-label="Notifications"
          >
            <Icon name="bell" />

            <span className="notification-count">
              2
            </span>
          </button>

          {/* User */}
          <div className="header-user">
            <div className="header-avatar">
              {initials}
            </div>

            <div className="header-user-info">
              <strong>{userName}</strong>

              <span>
                {role === "doctor" ? "Doctor" : "Patient"}
              </span>
            </div>
          </div>
        </header>

        <main className="dashboard-content">
          {children}
        </main>
      </div>
    </div>
  )
}

export default DashboardLayout