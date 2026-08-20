import { useEffect, useState } from "react";
import api from "../services/api";

function Dashboard() {
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const loadDashboard = async () => {
      try {
        setLoading(true);
        const response = await api.get("/dashboard/summary");
        setSummary(response.data);
      } catch (err) {
        console.error(err);
        setError(err.response?.data?.detail || "Unable to load dashboard data.");
      } finally {
        setLoading(false);
      }
    };
    loadDashboard();
  }, []);

  if (loading) {
    return (
      <div className="page">
        <div className="page-header">
          <div>
            <h1>Dashboard</h1>
            <p>Overview of your gym's performance.</p>
          </div>
        </div>
        <div className="dashboard-grid">
          {Array.from({ length: 9 }).map((_, index) => (
            <div className="dashboard-card skeleton-card" key={index}>
              <span className="skeleton-line" />
              <span className="skeleton-line short" />
            </div>
          ))}
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="page">
        <div className="page-header">
          <div>
            <h1>Dashboard</h1>
            <p>Overview of your gym's performance.</p>
          </div>
        </div>
        <div className="error-message">{error}</div>
      </div>
    );
  }

  const cards = [
    { title: "Total Members", value: summary?.total_members ?? 0 },
    { title: "Active Members", value: summary?.active_members ?? 0 },
    { title: "Expired Memberships", value: summary?.expired_memberships ?? 0 },
    { title: "Today's Revenue", value: `Rs. ${summary?.today_revenue ?? 0}` },
    { title: "Monthly Revenue", value: `Rs. ${summary?.monthly_revenue ?? 0}` },
    { title: "Monthly Expenses", value: `Rs. ${summary?.monthly_expenses ?? 0}` },
    { title: "Monthly Profit", value: `Rs. ${summary?.monthly_profit ?? 0}` },
    { title: "Trainers", value: summary?.total_trainers ?? 0 },
    { title: "Today's Attendance", value: summary?.today_attendance ?? 0 },
  ];

  const expiringCount = summary?.expiring_soon?.length ?? 0;

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h1>Dashboard</h1>
          <p>Overview of your gym's performance.</p>
        </div>
      </div>

      <div className="dashboard-grid">
        {cards.map((card) => (
          <div className="dashboard-card" key={card.title}>
            <span>{card.title}</span>
            <strong>{card.value}</strong>
          </div>
        ))}
      </div>

      <div className="dashboard-section">
        <h2>Memberships Expiring Soon</h2>
        {summary?.expiring_soon?.length ? (
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Member</th>
                  <th>Expiry Date</th>
                </tr>
              </thead>
              <tbody>
                {summary.expiring_soon.map((membership) => (
                  <tr key={membership.id}>
                    <td>
                      {membership.member_name ||
                        membership.full_name ||
                        membership.member_id}
                    </td>
                    <td>
                      {membership.end_date ||
                        membership.expiry_date ||
                        "-"}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <p>No memberships are expiring soon.</p>
        )}
        {expiringCount > 0 && (
          <div style={{ marginTop: "12px" }}>
            <a href="/reminders" style={{ color: "#17202a", fontWeight: 600 }}>
              View all reminders ({expiringCount})
            </a>
          </div>
        )}
      </div>
    </div>
  );
}

export default Dashboard;
