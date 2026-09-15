import { NavLink, Link } from "react-router-dom"

function DashboardLayout({
  children,
  role = "patient",
  userName = "Kabir Malhotra",
}) {

  const patientLinks = [
    {
      name: "Dashboard",
      path: "/patient/dashboard",
      icon: "⌂",
    },
    {
      name: "Emergency Passport",
      path: "/patient/passport",
      icon: "🪪",
    },
    {
      name: "Medical Timeline",
      path: "/patient/timeline",
      icon: "◷",
    },
    {
      name: "Documents",
      path: "/patient/documents",
      icon: "▤",
    },
    {
      name: "Access Control",
      path: "/patient/access",
      icon: "🔐",
    },
    {
      name: "Access History",
      path: "/patient/access-history",
      icon: "◉",
    },
  ]

  const doctorLinks = [
    {
      name: "Dashboard",
      path: "/doctor/dashboard",
      icon: "⌂",
    },
    {
      name: "Patients",
      path: "/doctor/patients",
      icon: "♙",
    },
    {
      name: "Emergency Passport",
      path: "/doctor/passport",
      icon: "🪪",
    },
    {
      name: "Medical Timeline",
      path: "/doctor/timeline",
      icon: "◷",
    },
    {
      name: "Documents",
      path: "/doctor/documents",
      icon: "▤",
    },
    {
      name: "AI Reviews",
      path: "/doctor/ai-reviews",
      icon: "✦",
    },
    {
      name: "Integrity",
      path: "/doctor/integrity",
      icon: "✓",
    },
    {
      name: "Emergency",
      path: "/doctor/emergency",
      icon: "🚨",
    },
    {
      name: "Audit Trail",
      path: "/doctor/audit",
      icon: "◉",
    },
  ]

  const links = role === "doctor"
    ? doctorLinks
    : patientLinks

  return (
    <div className="dashboard-layout">

      {/* SIDEBAR */}

      <aside className="dashboard-sidebar">

        <Link
          to="/"
          className="dashboard-logo"
        >
          Medi<span>-</span>Trace
        </Link>

        <div className="sidebar-subtitle">
          Emergency Health Platform
        </div>

        <nav className="sidebar-navigation">

          <div className="navigation-label">
            {role === "doctor"
              ? "CLINICAL"
              : "MY HEALTH"}
          </div>

          {links.map((link) => (

            <NavLink
              key={link.path}
              to={link.path}
              className={({ isActive }) =>
                `sidebar-link ${
                  isActive ? "active" : ""
                }`
              }
            >

              <span className="sidebar-icon">
                {link.icon}
              </span>

              <span>
                {link.name}
              </span>

            </NavLink>

          ))}

        </nav>

        {/* SIDEBAR BOTTOM */}

        <div className="sidebar-bottom">

          <NavLink
            to={`/${role}/profile`}
            className={({ isActive }) =>
              `sidebar-link ${
                isActive ? "active" : ""
              }`
            }
          >

            <span className="sidebar-icon">
              ⚙
            </span>

            Profile & Settings

          </NavLink>

          <Link
            to="/"
            className="sidebar-link logout-link"
          >

            <span className="sidebar-icon">
              ↪
            </span>

            Logout

          </Link>

        </div>

      </aside>

      {/* MAIN AREA */}

      <div className="dashboard-main">

        {/* HEADER */}

        <header className="dashboard-header">

          <div className="mobile-logo">

            <Link to="/">
              Medi<span>-</span>Trace
            </Link>

          </div>

          <div className="header-spacer"></div>

          {/* Emergency Status */}

          <div className="header-emergency-status">

            <span className="status-dot"></span>

            Emergency Ready

          </div>

          {/* Notification */}

          <button
            type="button"
            className="notification-button"
          >

            🔔

            <span className="notification-count">
              2
            </span>

          </button>

          {/* User */}

          <div className="header-user">

            <div className="header-avatar">

              {userName
                .split(" ")
                .map((word) => word[0])
                .join("")
                .slice(0, 2)
                .toUpperCase()
              }

            </div>

            <div className="header-user-info">

              <strong>
                {userName}
              </strong>

              <span>
                {role === "doctor"
                  ? "Doctor"
                  : "Patient"}
              </span>

            </div>

          </div>

        </header>

        {/* PAGE CONTENT */}

        <main className="dashboard-content">

          {children}

        </main>

      </div>

    </div>
  )
}

export default DashboardLayout