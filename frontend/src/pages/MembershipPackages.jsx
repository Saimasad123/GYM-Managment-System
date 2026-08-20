import { useEffect, useState } from "react";
import api from "../services/api";

const emptyForm = {
  name: "",
  duration_months: "",
  price: "",
  description: "",
};

function MembershipPackages() {
  const [packages, setPackages] = useState([]);
  const [form, setForm] = useState(emptyForm);
  const [editingId, setEditingId] = useState(null);

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const loadPackages = async () => {
    try {
      setLoading(true);
      setError("");

      const response = await api.get("/membership-packages");
      setPackages(response.data);
    } catch (err) {
      console.error(err);
      setError(
        err.response?.data?.detail ||
          "Unable to load packages."
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadPackages();
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
        duration_months: Number(form.duration_months),
        price: Number(form.price),
        description: form.description || null,
      };

      if (editingId) {
        await api.patch(`/membership-packages/${editingId}`, payload);
        setSuccess("Package updated successfully.");
      } else {
        await api.post("/membership-packages", payload);
        setSuccess("Package created successfully.");
      }

      resetForm();
      await loadPackages();
    } catch (err) {
      console.error(err);
      setError(
        err.response?.data?.detail ||
          "Unable to save package."
      );
    } finally {
      setSaving(false);
    }
  };

  const handleEdit = (pkg) => {
    setEditingId(pkg.id);
    setForm({
      name: pkg.name || "",
      duration_months: pkg.duration_months || "",
      price: pkg.price || "",
      description: pkg.description || "",
    });
    setError("");
    setSuccess("");
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const handleDeactivate = async (pkg) => {
    const confirmed = window.confirm(
      `Deactivate package "${pkg.name}"?`
    );
    if (!confirmed) return;

    try {
      setError("");
      setSuccess("");
      await api.delete(`/membership-packages/${pkg.id}`);
      setSuccess("Package deactivated successfully.");
      await loadPackages();
    } catch (err) {
      console.error(err);
      setError(
        err.response?.data?.detail ||
          "Unable to deactivate package."
      );
    }
  };

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h1>Membership Packages</h1>
          <p>Create and manage membership plans.</p>
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
          {editingId ? "Edit Package" : "Add New Package"}
        </h2>
        <form onSubmit={handleSubmit}>
          <div className="form-grid">
            <div className="form-group">
              <label>Package Name *</label>
              <input
                name="name"
                value={form.name}
                onChange={handleChange}
                placeholder="e.g. Monthly Basic"
                required
              />
            </div>
            <div className="form-group">
              <label>Duration (Months) *</label>
              <input
                type="number"
                name="duration_months"
                value={form.duration_months}
                onChange={handleChange}
                min="1"
                required
              />
            </div>
            <div className="form-group">
              <label>Price (Rs.) *</label>
              <input
                type="number"
                name="price"
                value={form.price}
                onChange={handleChange}
                min="0"
                step="0.01"
                required
              />
            </div>
            <div className="form-group full-width">
              <label>Description</label>
              <textarea
                name="description"
                value={form.description}
                onChange={handleChange}
                placeholder="Package details..."
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
                  ? "Update Package"
                  : "Create Package"}
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
          <h2>All Packages</h2>
          <button
            className="secondary-button"
            onClick={loadPackages}
          >
            Refresh
          </button>
        </div>
        {loading ? (
          <p>Loading packages...</p>
        ) : packages.length === 0 ? (
          <p>No packages found.</p>
        ) : (
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Duration</th>
                  <th>Price</th>
                  <th>Description</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {packages.map((pkg) => (
                  <tr key={pkg.id}>
                    <td>{pkg.name}</td>
                    <td>{pkg.duration_months} months</td>
                    <td>Rs. {pkg.price}</td>
                    <td>{pkg.description || "-"}</td>
                    <td>
                      <span
                        className={
                          pkg.is_active
                            ? "status-active"
                            : "status-inactive"
                        }
                      >
                        {pkg.is_active
                          ? "Active"
                          : "Inactive"}
                      </span>
                    </td>
                    <td>
                      <div className="action-buttons">
                        <button
                          className="edit-button"
                          onClick={() =>
                            handleEdit(pkg)
                          }
                        >
                          Edit
                        </button>
                        {pkg.is_active && (
                          <button
                            className="danger-button"
                            onClick={() =>
                              handleDeactivate(pkg)
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

export default MembershipPackages;
