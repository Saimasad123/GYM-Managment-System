import { useEffect, useState } from "react";
import api from "../services/api";

function Expenses() {
  const [expenses, setExpenses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const [form, setForm] = useState({
    category: "",
    description: "",
    amount: "",
    payment_method: "",
    reference_number: "",
    notes: "",
  });

  const loadExpenses = async () => {
    try {
      setLoading(true);
      setError("");

      const response = await api.get("/expenses");
      setExpenses(response.data);
    } catch (err) {
      console.error(err);

      setError(
        err.response?.data?.detail ||
          "Unable to load expenses."
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadExpenses();
  }, []);

  const handleChange = (event) => {
    const { name, value } = event.target;

    setForm((previous) => ({
      ...previous,
      [name]: value,
    }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    setError("");
    setSuccess("");

    if (
      !form.category ||
      !form.description ||
      !form.amount ||
      !form.payment_method
    ) {
      setError(
        "Category, description, amount and payment method are required."
      );
      return;
    }

    try {
      setSaving(true);

      await api.post("/expenses", {
        category: form.category,
        description: form.description,
        amount: Number(form.amount),
        payment_method: form.payment_method,
        reference_number:
          form.reference_number || null,
        notes: form.notes || null,
      });

      setForm({
        category: "",
        description: "",
        amount: "",
        payment_method: "",
        reference_number: "",
        notes: "",
      });

      setSuccess("Expense added successfully.");

      await loadExpenses();
    } catch (err) {
      console.error(err);

      setError(
        err.response?.data?.detail ||
          "Unable to add expense."
      );
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (expenseId) => {
    const confirmed = window.confirm(
      "Are you sure you want to delete this expense?"
    );

    if (!confirmed) {
      return;
    }

    try {
      setError("");
      setSuccess("");

      await api.delete(`/expenses/${expenseId}`);

      setSuccess("Expense deleted successfully.");

      await loadExpenses();
    } catch (err) {
      console.error(err);

      setError(
        err.response?.data?.detail ||
          "Unable to delete expense."
      );
    }
  };

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h1>Expenses</h1>
          <p>Manage gym expenses and operating costs.</p>
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

      <div className="dashboard-section">
        <h2>Add Expense</h2>

        <form onSubmit={handleSubmit}>
          <div className="form-grid">
            <div className="form-group">
              <label>Category</label>
              <input
                type="text"
                name="category"
                value={form.category}
                onChange={handleChange}
                placeholder="e.g. Utilities"
              />
            </div>

            <div className="form-group">
              <label>Description</label>
              <input
                type="text"
                name="description"
                value={form.description}
                onChange={handleChange}
                placeholder="e.g. Electricity bill"
              />
            </div>

            <div className="form-group">
              <label>Amount</label>
              <input
                type="number"
                name="amount"
                value={form.amount}
                onChange={handleChange}
                min="1"
                step="0.01"
                placeholder="25000"
              />
            </div>

            <div className="form-group">
              <label>Payment Method</label>
              <select
                name="payment_method"
                value={form.payment_method}
                onChange={handleChange}
              >
                <option value="">Select method</option>
                <option value="Cash">Cash</option>
                <option value="Bank Transfer">
                  Bank Transfer
                </option>
                <option value="Card">Card</option>
                <option value="Online">Online</option>
              </select>
            </div>

            <div className="form-group">
              <label>Reference Number</label>
              <input
                type="text"
                name="reference_number"
                value={form.reference_number}
                onChange={handleChange}
                placeholder="Optional"
              />
            </div>

            <div className="form-group">
              <label>Notes</label>
              <input
                type="text"
                name="notes"
                value={form.notes}
                onChange={handleChange}
                placeholder="Optional"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={saving}
          >
            {saving ? "Saving..." : "Add Expense"}
          </button>
        </form>
      </div>

      <div className="dashboard-section">
        <h2>Expense Records</h2>

        {loading ? (
          <p>Loading expenses...</p>
        ) : expenses.length === 0 ? (
          <p>No expenses found.</p>
        ) : (
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Category</th>
                  <th>Description</th>
                  <th>Amount</th>
                  <th>Payment Method</th>
                  <th>Reference</th>
                  <th>Date</th>
                  <th>Action</th>
                </tr>
              </thead>

              <tbody>
                {expenses.map((expense) => (
                  <tr key={expense.id}>
                    <td>{expense.category}</td>
                    <td>{expense.description}</td>
                    <td>
                      Rs. {expense.amount}
                    </td>
                    <td>
                      {expense.payment_method}
                    </td>
                    <td>
                      {expense.reference_number || "-"}
                    </td>
                    <td>
                      {expense.expense_date
                        ? new Date(
                            expense.expense_date
                          ).toLocaleDateString()
                        : "-"}
                    </td>
                    <td>
                      <button
                        type="button"
                        onClick={() =>
                          handleDelete(expense.id)
                        }
                      >
                        Delete
                      </button>
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

export default Expenses;