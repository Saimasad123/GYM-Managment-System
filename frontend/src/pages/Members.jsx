import { useEffect, useState } from "react";
import api from "../services/api";

const emptyForm = {
  member_code: "",
  full_name: "",
  father_name: "",
  phone: "",
  cnic: "",
  date_of_birth: "",
  gender: "",
  address: "",
  emergency_contact: "",
};

function Members() {
  const [members, setMembers] = useState([]);
  const [form, setForm] = useState(emptyForm);
  const [editingId, setEditingId] = useState(null);

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const loadMembers = async () => {
    try {
      setLoading(true);
      setError("");

      const response = await api.get("/members");
      setMembers(response.data);
    } catch (err) {
      console.error(err);
      setError(
        err.response?.data?.detail ||
          "Unable to load members."
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadMembers();
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
        father_name: form.father_name || null,
        cnic: form.cnic || null,
        date_of_birth: form.date_of_birth || null,
        gender: form.gender || null,
        address: form.address || null,
        emergency_contact: form.emergency_contact || null,
      };

      if (editingId) {
        await api.patch(`/members/${editingId}`, payload);
        setSuccess("Member updated successfully.");
      } else {
        await api.post("/members", payload);
        setSuccess("Member added successfully.");
      }

      resetForm();
      await loadMembers();
    } catch (err) {
      console.error(err);

      setError(
        err.response?.data?.detail ||
          "Unable to save member."
      );
    } finally {
      setSaving(false);
    }
  };

  const handleEdit = (member) => {
    setEditingId(member.id);

    setForm({
      member_code: member.member_code || "",
      full_name: member.full_name || "",
      father_name: member.father_name || "",
      phone: member.phone || "",
      cnic: member.cnic || "",
      date_of_birth: member.date_of_birth || "",
      gender: member.gender || "",
      address: member.address || "",
      emergency_contact: member.emergency_contact || "",
    });

    setError("");
    setSuccess("");

    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  };

  const handleDeactivate = async (member) => {
    const confirmed = window.confirm(
      `Deactivate ${member.full_name}?`
    );

    if (!confirmed) {
      return;
    }

    try {
      setError("");
      setSuccess("");

      await api.delete(`/members/${member.id}`);

      setSuccess("Member deactivated successfully.");

      await loadMembers();
    } catch (err) {
      console.error(err);

      setError(
        err.response?.data?.detail ||
          "Unable to deactivate member."
      );
    }
  };

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h1>Members</h1>
          <p>Manage gym members and their information.</p>
        </div>
      </div>

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      {success && (
        <div className="success-message">
          {success}
        </div>
      )}

      <div className="form-card">
        <h2>
          {editingId ? "Edit Member" : "Add New Member"}
        </h2>

        <form onSubmit={handleSubmit}>
          <div className="form-grid">
            <div className="form-group">
              <label>Member Code *</label>
              <input
                name="member_code"
                value={form.member_code}
                onChange={handleChange}
                placeholder="e.g. GYM-001"
                required
              />
            </div>

            <div className="form-group">
              <label>Full Name *</label>
              <input
                name="full_name"
                value={form.full_name}
                onChange={handleChange}
                placeholder="Member full name"
                required
              />
            </div>

            <div className="form-group">
              <label>Father Name</label>
              <input
                name="father_name"
                value={form.father_name}
                onChange={handleChange}
                placeholder="Father name"
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
              <label>CNIC</label>
              <input
                name="cnic"
                value={form.cnic}
                onChange={handleChange}
                placeholder="XXXXX-XXXXXXX-X"
              />
            </div>

            <div className="form-group">
              <label>Date of Birth</label>
              <input
                type="date"
                name="date_of_birth"
                value={form.date_of_birth}
                onChange={handleChange}
              />
            </div>

            <div className="form-group">
              <label>Gender</label>
              <select
                name="gender"
                value={form.gender}
                onChange={handleChange}
              >
                <option value="">Select gender</option>
                <option value="Male">Male</option>
                <option value="Female">Female</option>
                <option value="Other">Other</option>
              </select>
            </div>

            <div className="form-group">
              <label>Emergency Contact</label>
              <input
                name="emergency_contact"
                value={form.emergency_contact}
                onChange={handleChange}
                placeholder="Emergency contact"
              />
            </div>

            <div className="form-group full-width">
              <label>Address</label>
              <textarea
                name="address"
                value={form.address}
                onChange={handleChange}
                placeholder="Member address"
                rows="3"
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
                  ? "Update Member"
                  : "Add Member"}
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
          <h2>All Members</h2>

          <button
            className="secondary-button"
            onClick={loadMembers}
          >
            Refresh
          </button>
        </div>

        {loading ? (
          <p>Loading members...</p>
        ) : members.length === 0 ? (
          <p>No members found.</p>
        ) : (
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Code</th>
                  <th>Name</th>
                  <th>Phone</th>
                  <th>CNIC</th>
                  <th>Gender</th>
                  <th>Joining Date</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>

              <tbody>
                {members.map((member) => (
                  <tr key={member.id}>
                    <td>{member.member_code}</td>
                    <td>{member.full_name}</td>
                    <td>{member.phone}</td>
                    <td>{member.cnic || "-"}</td>
                    <td>{member.gender || "-"}</td>
                    <td>{member.joining_date}</td>

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
                              handleDeactivate(member)
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

export default Members;