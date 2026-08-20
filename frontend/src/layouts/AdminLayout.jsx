import { NavLink, Outlet, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

function AdminLayout() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login", { replace: true });
  };

  const navigation = [
    { path: "/dashboard", label: "Dashboard" },
    { path: "/members", label: "Members" },
    { path: "/membership-packages", label: "Membership Packages" },
    { path: "/membership-status", label: "Membership Status" },
    { path: "/memberships", label: "Memberships" },
    { path: "/payments", label: "Payments" },
    { path: "/expenses", label: "Expenses" },
    { path: "/attendance", label: "Attendance" },
    { path: "/trainers", label: "Trainers" },
    { path: "/staff", label: "Staff" },
    { path: "/reminders", label: "Reminders" },
    { path: "/financial-reports", label: "Financial Reports" }
    
  ];

  return (
    <div className="admin-layout">
      <aside className="sidebar">
        <div className="sidebar-brand">
          <div className="brand-logo">GYM</div>
          <div>
            <strong>Gym Manager</strong>
            <span>Admin Panel</span>
          </div>
        </div>

        <nav className="sidebar-nav">
          {navigation.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                isActive ? "nav-link active" : "nav-link"
              }
            >
              {item.label}
            </NavLink>
          ))}
        </nav>

        <button className="logout-button" onClick={handleLogout}>
          Logout
        </button>
      </aside>

      <div className="main-area">
        <header className="topbar">
          <div>
            <h2>Gym Management System</h2>
          </div>

          <div className="user-info">
            <span>Admin</span>
            <strong>{user?.username || "Administrator"}</strong>
          </div>
        </header>

        <main className="content">
          <Outlet />
        </main>
      </div>
    </div>
  );
}

export default AdminLayout;
