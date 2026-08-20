import { useEffect, useState } from "react";
import api from "../services/api";

const emptyForm = {
  member_id: "",
  package_id: "",
  start_date: "",
  amount_paid: "",
};

function Memberships() {
  const [memberships, setMemberships] = useState([]);
  const [members, setMembers] = useState([]);
  const [packages, setPackages] = useState([]);
  const [form, setForm] = useState(emptyForm);
  const [editingId, setEditingId] = useState(null);

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const loadData = async () => {
    try {
      setLoading(true);
      setError("");

      const [membershipsRes, membersRes, packagesRes] =
        await Promise.all([
          api.get("/memberships"),
          api.get("/members?page_size=1000"),
          api.get("/membership-packages"),
        ]);

      setMemberships(membershipsRes.data);
      setMembers(membersRes.data);
      setPackages(
        packagesRes.data.filter((pkg) => pkg.is_active)
      );
    } catch (err) {
      console.error(err);
      setError(
        err.response?.data?.detail ||
          "Unable to load memberships."
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setForm((previous) => ({
      ...previous,
      [name]: value,
    }));
  };

  const resetForm = () => {
    setForm(emptyForm);
    setEditingId(null);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");
    setSuccess("");
    setSaving(true);

    try {
      const payload = {
        member_id: Number(form.member_id),
        package_id: Number(form.package_id),
        start_date: form.start_date,
        amount_paid: Number(form.amount_paid),
      };

      if (editingId) {
        await api.patch(
          `/memberships/${editingId}`,
          payload
        );
        setSuccess("Membership updated successfully.");
      } else {
        await api.post("/memberships", payload);
        setSuccess("Membership created successfully.");
      }

      resetForm();
      await loadData();
    } catch (err) {
      console.error(err);
      setError(
        err.response?.data?.detail ||
          "Unable to save membership."
      );
    } finally {
      setSaving(false);
    }
  };

  const handleRenew = async (membershipId) => {
    const confirmed = window.confirm(
      "Renew this membership from its expiry date?"
    );
    if (!confirmed) return;

    try {
      setError("");
      setSuccess("");

      await api.post(
        `/memberships/${membershipId}/renew`
      );

      setSuccess("Membership renewed successfully.");
      await loadData();
    } catch (err) {
      console.error(err);
      setError(
        err.response?.data?.detail ||
          "Unable to renew membership."
      );
    }
  };

  const getMemberName = (membership) => {
    if (membership.member?.full_name) {
      return membership.member.full_name;
    }
    return `Member #${membership.member_id}`;
  };

  const getPackageName = (membership) => {
    if (membership.package?.name) {
      return membership.package.name;
    }
    return `Package #${membership.package_id}`;
  };

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h1>Memberships</h1>
          <p>Manage member memberships and renewals.</p>
        </div>
      </div>

      {error && (
        <div className="error-message">{error}</div>
      )}
      {success && (
        <div className="success-message">{success}</div>
      )}

      <div className="form-card">
        <h2>
          {editingId
            ? "Edit Membership"
            : "Add New Membership"}
        </h2>
        <form onSubmit={handleSubmit}>
          <div className="form-grid">
            <div className="form-group">
              <label>Member *</label>
              <select
                name="member_id"
                value={form.member_id}
                onChange={handleChange}
                required
              >
                <option value="">
                  Select member
                </option>
                {members.map((member) => (
                  <option
                    key={member.id}
                    value={member.id}
                  >
                    {member.full_name} (
                    {member.member_code})
                  </option>
                ))}
              </select>
            </div>
            <div className="form-group">
              <label>Package *</label>
              <select
                name="package_id"
                value={form.package_id}
                onChange={handleChange}
                required
              >
                <option value="">
                  Select package
                </option>
                {packages.map((pkg) => (
                  <option
                    key={pkg.id}
                    value={pkg.id}
                  >
                    {pkg.name} - Rs. {pkg.price} (
                    {pkg.duration_months} months)
                  </option>
                ))}
              </select>
            </div>
            <div className="form-group">
              <label>Start Date *</label>
              <input
                type="date"
                name="start_date"
                value={form.start_date}
                onChange={handleChange}
                required
              />
            </div>
            <div className="form-group">
              <label>Amount Paid (Rs.) *</label>
              <input
                type="number"
                name="amount_paid"
                value={form.amount_paid}
                onChange={handleChange}
                min="0"
                step="0.01"
                required
              />
            </div>
          </div>
          <div className="form-actions">
            <button
              type="submit"
              disabled={saving}
              className="primary-button"
            >
              {saving
                ? "Saving..."
                : editingId
                  ? "Update Membership"
                  : "Create Membership"}
            </button>
            {editingId && (
              <button
                type="button"
                className="secondary-button"
                onClick={resetForm}
              >
                Cancel
              </button>
            )}
          </div>
        </form>
      </div>

      <div className="table-card">
        <div className="table-header">
          <h2>All Memberships</h2>
          <button
            className="secondary-button"
            onClick={loadData}
          >
            Refresh
          </button>
        </div>
        {loading ? (
          <p>Loading memberships...</p>
        ) : memberships.length === 0 ? (
          <p>No memberships found.</p>
        ) : (
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Member</th>
                  <th>Package</th>
                  <th>Start Date</th>
                  <th>Expiry Date</th>
                  <th>Total Fee</th>
                  <th>Paid</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {memberships.map((membership) => (
                  <tr key={membership.id}>
                    <td>
                      {getMemberName(membership)}
                    </td>
                    <td>
                      {getPackageName(membership)}
                    </td>
                    <td>
                      {membership.start_date}
                    </td>
                    <td>
                      {membership.expiry_date}
                    </td>
                    <td>
                      Rs. {membership.total_fee}
                    </td>
                    <td>
                      Rs. {membership.amount_paid}
                    </td>
                    <td>
                      <span
                        className={
                          membership.status ===
                          "active"
                            ? "status-active"
                            : "status-inactive"
                        }
                      >
                        {membership.status}
                      </span>
                    </td>
                    <td>
                      <div className="action-buttons">
                        <button
                          className="primary-button"
                          onClick={() =>
                            handleRenew(
                              membership.id
                            )
                          }
                        >
                          Renew
                        </button>
                      </div>
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

export default Memberships;
