import { useEffect, useState } from "react";
import api from "../services/api";

const emptyForm = {
  trainer_code: "",
  full_name: "",
  phone: "",
  specialization: "",
  salary: "",
  joining_date: "",
};

function Trainers() {
  const [trainers, setTrainers] = useState([]);
  const [form, setForm] = useState(emptyForm);
  const [editingId, setEditingId] = useState(null);

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const loadTrainers = async () => {
    try {
      setLoading(true);
      setError("");

      const response = await api.get("/trainers");
      setTrainers(response.data);
    } catch (err) {
      console.error(err);
      setError(
        err.response?.data?.detail ||
          "Unable to load trainers."
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadTrainers();
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
        salary: Number(form.salary),
        specialization: form.specialization || null,
        joining_date: form.joining_date || undefined,
      };

      if (editingId) {
        await api.patch(
          `/trainers/${editingId}`,
          payload
        );
        setSuccess("Trainer updated successfully.");
      } else {
        await api.post("/trainers", payload);
        setSuccess("Trainer added successfully.");
      }

      resetForm();
      await loadTrainers();
    } catch (err) {
      console.error(err);
      setError(
        err.response?.data?.detail ||
          "Unable to save trainer."
      );
    } finally {
      setSaving(false);
    }
  };

  const handleEdit = (trainer) => {
    setEditingId(trainer.id);
    setForm({
      trainer_code: trainer.trainer_code || "",
      full_name: trainer.full_name || "",
      phone: trainer.phone || "",
      specialization:
        trainer.specialization || "",
      salary: trainer.salary || "",
      joining_date: trainer.joining_date || "",
    });
    setError("");
    setSuccess("");
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const handleDeactivate = async (trainer) => {
    const confirmed = window.confirm(
      `Deactivate trainer ${trainer.full_name}?`
    );
    if (!confirmed) return;

    try {
      setError("");
      setSuccess("");
      await api.delete(`/trainers/${trainer.id}`);
      setSuccess("Trainer deactivated successfully.");
      await loadTrainers();
    } catch (err) {
      console.error(err);
      setError(
        err.response?.data?.detail ||
          "Unable to deactivate trainer."
      );
    }
  };

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h1>Trainers</h1>
          <p>Manage gym trainers and staff.</p>
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
            ? "Edit Trainer"
            : "Add New Trainer"}
        </h2>
        <form onSubmit={handleSubmit}>
          <div className="form-grid">
            <div className="form-group">
              <label>Trainer Code *</label>
              <input
                name="trainer_code"
                value={form.trainer_code}
                onChange={handleChange}
                placeholder="e.g. TR-001"
                required
              />
            </div>
            <div className="form-group">
              <label>Full Name *</label>
              <input
                name="full_name"
                value={form.full_name}
                onChange={handleChange}
                placeholder="Trainer full name"
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
              <label>Specialization</label>
              <input
                name="specialization"
                value={form.specialization}
                onChange={handleChange}
                placeholder="e.g. Strength Training"
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
                  ? "Update Trainer"
                  : "Add Trainer"}
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
          <h2>All Trainers</h2>
          <button
            className="secondary-button"
            onClick={loadTrainers}
          >
            Refresh
          </button>
        </div>
        {loading ? (
          <p>Loading trainers...</p>
        ) : trainers.length === 0 ? (
          <p>No trainers found.</p>
        ) : (
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Code</th>
                  <th>Name</th>
                  <th>Phone</th>
                  <th>Specialization</th>
                  <th>Salary</th>
                  <th>Joining Date</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {trainers.map((trainer) => (
                  <tr key={trainer.id}>
                    <td>
                      {trainer.trainer_code}
                    </td>
                    <td>{trainer.full_name}</td>
                    <td>{trainer.phone}</td>
                    <td>
                      {trainer.specialization ||
                        "-"}
                    </td>
                    <td>
                      Rs. {trainer.salary}
                    </td>
                    <td>
                      {trainer.joining_date}
                    </td>
                    <td>
                      <span
                        className={
                          trainer.is_active
                            ? "status-active"
                            : "status-inactive"
                        }
                      >
                        {trainer.is_active
                          ? "Active"
                          : "Inactive"}
                      </span>
                    </td>
                    <td>
                      <div className="action-buttons">
                        <button
                          className="edit-button"
                          onClick={() =>
                            handleEdit(
                              trainer
                            )
                          }
                        >
                          Edit
                        </button>
                        {trainer.is_active && (
                          <button
                            className="danger-button"
                            onClick={() =>
                              handleDeactivate(
                                trainer
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

export default Trainers;
