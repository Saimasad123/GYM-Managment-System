import { useEffect, useState } from "react";
import api from "../services/api";

function Reminders() {
  const [upcoming, setUpcoming] = useState([]);
  const [allReminders, setAllReminders] = useState([]);
  const [daysFilter, setDaysFilter] = useState(2);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const loadUpcoming = async () => {
    try {
      setLoading(true);
      setError("");

      const response = await api.get(
        "/reminders/upcoming",
        {
          params: { days: daysFilter },
        }
      );

      setUpcoming(response.data || []);
    } catch (err) {
      console.error(err);
      setError(
        err.response?.data?.detail ||
          "Unable to load upcoming reminders."
      );
      setUpcoming([]);
    } finally {
      setLoading(false);
    }
  };

  const loadAllReminders = async () => {
    try {
      const response = await api.get("/reminders");
      setAllReminders(response.data || []);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    loadUpcoming();
    loadAllReminders();
  }, [daysFilter]);

  const handleSendReminder = async (reminderId) => {
    try {
      setSaving(true);
      setError("");

      await api.patch(`/reminders/${reminderId}/send`);
      setSuccess("Reminder marked as sent.");
      await Promise.all([loadUpcoming(), loadAllReminders()]);
    } catch (err) {
      console.error(err);
      setError(
        err.response?.data?.detail ||
          "Unable to send reminder."
      );
    } finally {
      setSaving(false);
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return "-";
    return new Date(dateString + "T00:00:00").toLocaleDateString();
  };

  if (loading && upcoming.length === 0) {
    return (
      <div className="page">
        <div className="page-header">
          <div>
            <h1>Reminders</h1>
            <p>
              Manage membership expiration reminders.
            </p>
          </div>
        </div>
        <p>Loading reminders...</p>
      </div>
    );
  }

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h1>Reminders</h1>
          <p>
            Manage membership expiration reminders.
          </p>
        </div>
        <div style={{ display: "flex", gap: "10px", alignItems: "center" }}>
          <select
            value={daysFilter}
            onChange={(e) =>
              setDaysFilter(Number(e.target.value))
            }
            style={{
              padding: "8px 12px",
              border: "1px solid #d1d5db",
              borderRadius: "8px",
            }}
          >
            <option value="1">1 day</option>
            <option value="2">2 days</option>
            <option value="3">3 days</option>
            <option value="7">7 days</option>
          </select>
          <button
            className="secondary-button"
            onClick={loadUpcoming}
          >
            Refresh
          </button>
        </div>
      </div>

      {error && (
        <div className="error-message">{error}</div>
      )}
      {success && (
        <div className="success-message">{success}</div>
      )}

      <div className="dashboard-section">
        <h2>
          Upcoming Expirations ({upcoming.length})
        </h2>
        {upcoming.length === 0 ? (
          <p>
            No memberships are expiring in the next {daysFilter} day(s).
          </p>
        ) : (
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Member</th>
                  <th>Package</th>
                  <th>Expiry Date</th>
                  <th>Days Remaining</th>
                  <th>Reminder</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                {upcoming.map((item) => (
                  <tr key={item.id}>
                    <td>
                      {item.member_name ||
                        `Member #${item.member_id}`}
                      <br />
                      <small style={{ color: "#6b7280" }}>
                        {item.member_code}
                      </small>
                    </td>
                    <td>{item.package_name}</td>
                    <td>
                      {formatDate(item.expiry_date)}
                    </td>
                    <td>
                      <span
                        className={
                          item.days_remaining <= 1
                            ? "status-inactive"
                            : "status-warning"
                        }
                        style={{ fontWeight: 600 }}
                      >
                        {item.days_remaining} day(s)
                      </span>
                    </td>
                    <td>{item.message}</td>
                    <td>
                      <button
                        className="primary-button"
                        onClick={() =>
                          handleSendReminder(
                            item.id
                          )
                        }
                        disabled={saving}
                      >
                        Send Reminder
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      <div className="dashboard-section">
        <h2>All Reminders</h2>
        {allReminders.length === 0 ? (
          <p>No reminders found.</p>
        ) : (
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Membership ID</th>
                  <th>Reminder Date</th>
                  <th>Type</th>
                  <th>Message</th>
                  <th>Status</th>
                  <th>Sent At</th>
                </tr>
              </thead>
              <tbody>
                {allReminders.map((reminder) => (
                  <tr key={reminder.id}>
                    <td>
                      {reminder.membership_id}
                    </td>
                    <td>
                      {formatDate(
                        reminder.reminder_date
                      )}
                    </td>
                    <td>
                      {reminder.reminder_type}
                    </td>
                    <td>{reminder.message}</td>
                    <td>
                      <span
                        className={
                          reminder.is_sent
                            ? "status-active"
                            : "status-warning"
                        }
                      >
                        {reminder.is_sent
                          ? "Sent"
                          : "Pending"}
                      </span>
                    </td>
                    <td>
                      {reminder.sent_at
                        ? formatDate(
                            reminder.sent_at
                          )
                        : "-"}
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

export default Reminders;
