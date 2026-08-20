import { useEffect, useState } from "react";
import api from "../services/api";

function MembershipStatus() {
  const [memberships, setMemberships] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const loadData = async () => {
    try {
      setLoading(true);
      setError("");

      const response = await api.get("/memberships/status", {
        timeout: 15000,
      });

      setMemberships(response.data || []);
    } catch (err) {
      console.error("Failed to load membership status:", err);
      setError(
        err.response?.data?.detail ||
          err.message ||
          "Unable to load membership status."
      );
      setMemberships([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const formatCurrency = (value) => {
    const num = Number(value);
    return `Rs. ${num.toLocaleString()}`;
  };

  const getStatusClass = (status) => {
    switch (status) {
      case "Active":
        return "status-active";
      case "Expiring Soon":
        return "status-warning";
      case "Expired":
        return "status-inactive";
      default:
        return "";
    }
  };

  const getPaymentClass = (status) => {
    switch (status) {
      case "Paid":
        return "status-active";
      case "Partial":
        return "status-warning";
      case "Unpaid":
        return "status-inactive";
      default:
        return "";
    }
  };

  if (loading) {
    return (
      <div className="page">
        <div className="page-header">
          <div>
            <h1>Membership Status</h1>
            <p>
              Track all memberships, expiry and payment
              status.
            </p>
          </div>
        </div>

        <div className="dashboard-grid">
          {Array.from({ length: 3 }).map((_, index) => (
            <div
              className="dashboard-card skeleton-card"
              key={index}
            >
              <span className="skeleton-line" />
              <span className="skeleton-line short" />
            </div>
          ))}
        </div>

        <div className="dashboard-section">
          <div className="skeleton-line" style={{ width: "200px", marginBottom: "16px" }} />
          <div className="skeleton-line" style={{ width: "100%", height: "120px" }} />
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="page">
        <div className="page-header">
          <div>
            <h1>Membership Status</h1>
            <p>
              Track all memberships, expiry and payment
              status.
            </p>
          </div>
          <button
            className="secondary-button"
            onClick={loadData}
          >
            Retry
          </button>
        </div>
        <div className="error-message">{error}</div>
      </div>
    );
  }

  const activeCount = memberships.filter(
    (m) => m.membership_status === "Active"
  ).length;
  const expiringCount = memberships.filter(
    (m) => m.membership_status === "Expiring Soon"
  ).length;
  const expiredCount = memberships.filter(
    (m) => m.membership_status === "Expired"
  ).length;

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h1>Membership Status</h1>
          <p>
            Track all memberships, expiry and payment
            status.
          </p>
        </div>
        <button
          className="secondary-button"
          onClick={loadData}
        >
          Refresh
        </button>
      </div>

      <div className="dashboard-grid">
        <div className="dashboard-card">
          <span>Active Memberships</span>
          <strong>{activeCount}</strong>
        </div>
        <div className="dashboard-card">
          <span>Expiring Soon</span>
          <strong>{expiringCount}</strong>
        </div>
        <div className="dashboard-card">
          <span>Expired Memberships</span>
          <strong>{expiredCount}</strong>
        </div>
      </div>

      <div className="dashboard-section">
        <h2>All Memberships</h2>
        {memberships.length === 0 ? (
          <p>No memberships found.</p>
        ) : (
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Member</th>
                  <th>Package</th>
                  <th>Duration</th>
                  <th>Start Date</th>
                  <th>Expiry Date</th>
                  <th>Total Fee</th>
                  <th>Paid</th>
                  <th>Balance</th>
                  <th>Payment Status</th>
                  <th>Membership Status</th>
                  <th>Days Left</th>
                </tr>
              </thead>
              <tbody>
                {memberships.map((membership) => (
                  <tr key={membership.id}>
                    <td>
                      {membership.member_name ||
                        `Member #${membership.member_id}`}
                      <br />
                      <small style={{ color: "#6b7280" }}>
                        {membership.member_code}
                      </small>
                    </td>
                    <td>
                      {membership.package_name || "-"}
                    </td>
                    <td>
                      {membership.duration_months
                        ? `${membership.duration_months} months`
                        : "-"}
                    </td>
                    <td>
                      {membership.start_date || "-"}
                    </td>
                    <td>
                      {membership.expiry_date || "-"}
                    </td>
                    <td>
                      {formatCurrency(
                        membership.total_fee
                      )}
                    </td>
                    <td>
                      {formatCurrency(
                        membership.amount_paid
                      )}
                    </td>
                    <td>
                      {formatCurrency(
                        membership.balance
                      )}
                    </td>
                    <td>
                      <span
                        className={getPaymentClass(
                          membership.payment_status
                        )}
                      >
                        {membership.payment_status}
                      </span>
                    </td>
                    <td>
                      <span
                        className={getStatusClass(
                          membership.membership_status
                        )}
                      >
                        {membership.membership_status}
                      </span>
                    </td>
                    <td>
                      {membership.membership_status ===
                      "Expired"
                        ? "0"
                        : `${membership.days_remaining} days`}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}

export default MembershipStatus;
