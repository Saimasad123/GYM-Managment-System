import { useEffect, useState } from "react";
import api from "../services/api";

const emptyForm = {
  staff_code: "",
  full_name: "",
  phone: "",
  email: "",
  role: "",
  department: "",
  salary: "",
  joining_date: "",
};

function Staff() {
  const [staff, setStaff] = useState([]);
  const [form, setForm] = useState(emptyForm);
  const [editingId, setEditingId] = useState(null);

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const loadStaff = async () => {
    try {
      setLoading(true);
      setError("");

      const response = await api.get("/staff");
      setStaff(response.data);
    } catch (err) {
      console.error(err);
      setError(
        err.response?.data?.detail ||
          "Unable to load staff."
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadStaff();
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
        ...form,
        salary: form.salary ? Number(form.salary) : null,
        email: form.email || null,
        department: form.department || null,
        joining_date: form.joining_date || null,
      };

      if (editingId) {
        await api.patch(`/staff/${editingId}`, payload);
        setSuccess("Staff updated successfully.");
      } else {
        await api.post("/staff", payload);
        setSuccess("Staff added successfully.");
      }

      resetForm();
      await loadStaff();
    } catch (err) {
      console.error(err);
      setError(
        err.response?.data?.detail ||
          "Unable to save staff."
      );
    } finally {
      setSaving(false);
    }
  };

  const handleEdit = (member) => {
    setEditingId(member.id);
    setForm({
      staff_code: member.staff_code || "",
      full_name: member.full_name || "",
      phone: member.phone || "",
      email: member.email || "",
      role: member.role || "",
      department: member.department || "",
      salary: member.salary || "",
      joining_date: member.joining_date || "",
    });
    setError("");
    setSuccess("");
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const handleDeactivate = async (member) => {
    const confirmed = window.confirm(
      `Deactivate staff ${member.full_name}?`
    );
    if (!confirmed) return;

    try {
      setError("");
      setSuccess("");
      await api.delete(`/staff/${member.id}`);
      setSuccess("Staff deactivated successfully.");
      await loadStaff();
    } catch (err) {
      console.error(err);
      setError(
        err.response?.data?.detail ||
          "Unable to deactivate staff."
      );
    }
  };

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h1>Staff</h1>
          <p>Manage gym staff and employees.</p>
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
            ? "Edit Staff"
            : "Add New Staff"}
        </h2>
        <form onSubmit={handleSubmit}>
          <div className="form-grid">
            <div className="form-group">
              <label>Staff Code *</label>
              <input
                name="staff_code"
                value={form.staff_code}
                onChange={handleChange}
                placeholder="e.g. STF-001"
                required
              />
            </div>
            <div className="form-group">
              <label>Full Name *</label>
              <input
                name="full_name"
                value={form.full_name}
                onChange={handleChange}
                placeholder="Staff full name"
                required
              />
            </div>
            <div className="form-group">
              <label>Phone *</label>
              <input
                name="phone"
                value={form.phone}
                onChange={handleChange}
                placeholder="03XXXXXXXXX"
                required
              />
            </div>
            <div className="form-group">
              <label>Email</label>
              <input
                type="email"
                name="email"
                value={form.email}
                onChange={handleChange}
                placeholder="optional"
              />
            </div>
            <div className="form-group">
              <label>Role *</label>
              <input
                name="role"
                value={form.role}
                onChange={handleChange}
                placeholder="e.g. Receptionist"
                required
              />
            </div>
            <div className="form-group">
              <label>Department</label>
              <input
                name="department"
                value={form.department}
                onChange={handleChange}
                placeholder="e.g. Front Desk"
              />
            </div>
            <div className="form-group">
              <label>Salary (Rs.)</label>
              <input
                type="number"
                name="salary"
                value={form.salary}
                onChange={handleChange}
                min="0"
                step="0.01"
              />
            </div>
            <div className="form-group">
              <label>Joining Date</label>
              <input
                type="date"
                name="joining_date"
                value={form.joining_date}
                onChange={handleChange}
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
                  ? "Update Staff"
                  : "Add Staff"}
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
          <h2>All Staff</h2>
          <button
            className="secondary-button"
            onClick={loadStaff}
          >
            Refresh
          </button>
        </div>
        {loading ? (
          <p>Loading staff...</p>
        ) : staff.length === 0 ? (
          <p>No staff found.</p>
        ) : (
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Code</th>
                  <th>Name</th>
                  <th>Phone</th>
                  <th>Email</th>
                  <th>Role</th>
                  <th>Department</th>
                  <th>Salary</th>
                  <th>Joining Date</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {staff.map((member) => (
                  <tr key={member.id}>
                    <td>{member.staff_code}</td>
                    <td>{member.full_name}</td>
                    <td>{member.phone}</td>
                    <td>{member.email || "-"}</td>
                    <td>{member.role}</td>
                    <td>{member.department || "-"}</td>
                    <td>
                      {member.salary
                        ? `Rs. ${member.salary}`
                        : "-"}
                    </td>
                    <td>
                      {member.joining_date || "-"}
                    </td>
                    <td>
                      <span
                        className={
                          member.is_active
                            ? "status-active"
                            : "status-inactive"
                        }
                      >
                        {member.is_active
                          ? "Active"
                          : "Inactive"}
                      </span>
                    </td>
                    <td>
                      <div className="action-buttons">
                        <button
                          className="edit-button"
                          onClick={() =>
                            handleEdit(member)
                          }
                        >
                          Edit
                        </button>
                        {member.is_active && (
                          <button
                            className="danger-button"
                            onClick={() =>
                              handleDeactivate(
                                member
                              )
                            }
                          >
                            Deactivate
                          </button>
                        )}
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

export default Staff;
