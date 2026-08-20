import { useEffect, useState } from "react";
import api from "../services/api";

const emptyForm = {
  member_id: "",
  membership_id: "",
  amount: "",
  payment_method: "",
  reference_number: "",
  notes: "",
};

function Payments() {
  const [payments, setPayments] = useState([]);
  const [members, setMembers] = useState([]);
  const [form, setForm] = useState(emptyForm);

  const [selectedYear, setSelectedYear] = useState(
    new Date().getFullYear()
  );
  const [selectedMonth, setSelectedMonth] = useState(
    new Date().getMonth() + 1
  );

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const currentYear = new Date().getFullYear();
  const yearOptions = Array.from(
    { length: 11 },
    (_, i) => currentYear - 5 + i
  );

  const loadData = async () => {
    try {
      setLoading(true);
      setError("");

      const [paymentsRes, membersRes] =
        await Promise.all([
          api.get("/payments", {
            params: {
              year: selectedYear,
              month: selectedMonth,
            },
          }),
          api.get("/members?page_size=1000"),
        ]);

      setPayments(paymentsRes.data);
      setMembers(membersRes.data);
    } catch (err) {
      console.error(err);
      setError(
        err.response?.data?.detail ||
          "Unable to load payments."
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [selectedYear, selectedMonth]);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setForm((previous) => ({
      ...previous,
      [name]: value,
    }));
  };

  const resetForm = () => {
    setForm(emptyForm);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");
    setSuccess("");

    if (
      !form.member_id ||
      !form.amount ||
      !form.payment_method
    ) {
      setError(
        "Member, amount and payment method are required."
      );
      return;
    }

    try {
      setSaving(true);

      const payload = {
        member_id: Number(form.member_id),
        membership_id: form.membership_id
          ? Number(form.membership_id)
          : null,
        amount: Number(form.amount),
        payment_method: form.payment_method,
        reference_number:
          form.reference_number || null,
        notes: form.notes || null,
      };

      await api.post("/payments", payload);

      setForm(emptyForm);
      setSuccess("Payment recorded successfully.");
      await loadData();
    } catch (err) {
      console.error(err);
      setError(
        err.response?.data?.detail ||
          "Unable to record payment."
      );
    } finally {
      setSaving(false);
    }
  };

  const getMemberName = (memberId) => {
    const member = members.find(
      (m) => m.id === memberId
    );
    return member
      ? `${member.full_name} (${member.member_code})`
      : `Member #${memberId}`;
  };

  const formatDate = (dateString) => {
    if (!dateString) return "-";
    return new Date(dateString).toLocaleDateString();
  };

  const monthName = new Date(
    selectedYear,
    selectedMonth - 1,
    1
  ).toLocaleString("default", { month: "long" });

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h1>Payments</h1>
          <p>
            Record and track member payments.
          </p>
        </div>
      </div>

      {error && (
        <div className="error-message">{error}</div>
      )}
      {success && (
        <div className="success-message">{success}</div>
      )}

      <div className="dashboard-section">
        <h2>Record Payment</h2>
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
              <label>Amount (Rs.) *</label>
              <input
                type="number"
                name="amount"
                value={form.amount}
                onChange={handleChange}
                min="0"
                step="0.01"
                required
              />
            </div>
            <div className="form-group">
              <label>Payment Method *</label>
              <select
                name="payment_method"
                value={form.payment_method}
                onChange={handleChange}
                required
              >
                <option value="">
                  Select method
                </option>
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
            <div className="form-group full-width">
              <label>Notes</label>
              <textarea
                name="notes"
                value={form.notes}
                onChange={handleChange}
                placeholder="Optional"
                rows="2"
              />
            </div>
          </div>
          <button
            type="submit"
            disabled={saving}
            className="primary-button"
          >
            {saving
              ? "Saving..."
              : "Record Payment"}
          </button>
        </form>
      </div>

      <div className="dashboard-section">
        <div className="table-header">
          <h2>
            Payment History - {monthName}{" "}
            {selectedYear}
          </h2>
          <div style={{ display: "flex", gap: "10px", alignItems: "center" }}>
            <select
              value={selectedYear}
              onChange={(e) =>
                setSelectedYear(
                  Number(e.target.value)
                )
              }
              style={{
                padding: "8px 12px",
                border: "1px solid #d1d5db",
                borderRadius: "8px",
              }}
            >
              {yearOptions.map((year) => (
                <option
                  key={year}
                  value={year}
                >
                  {year}
                </option>
              ))}
            </select>
            <select
              value={selectedMonth}
              onChange={(e) =>
                setSelectedMonth(
                  Number(e.target.value)
                )
              }
              style={{
                padding: "8px 12px",
                border: "1px solid #d1d5db",
                borderRadius: "8px",
              }}
            >
              {Array.from({ length: 12 }, (_, i) => (
                <option
                  key={i + 1}
                  value={i + 1}
                >
                  {new Date(
                    selectedYear,
                    i,
                    1
                  ).toLocaleString(
                    "default",
                    { month: "long" }
                  )}
                </option>
              ))}
            </select>
            <button
              className="secondary-button"
              onClick={loadData}
            >
              Refresh
            </button>
          </div>
        </div>

        {loading ? (
          <p>Loading payments...</p>
        ) : payments.length === 0 ? (
          <p>No payments found for {monthName} {selectedYear}.</p>
        ) : (
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Member</th>
                  <th>Amount</th>
                  <th>Method</th>
                  <th>Reference</th>
                  <th>Notes</th>
                </tr>
              </thead>
              <tbody>
                {payments.map((payment) => (
                  <tr key={payment.id}>
                    <td>
                      {formatDate(
                        payment.payment_date
                      )}
                    </td>
                    <td>
                      {getMemberName(
                        payment.member_id
                      )}
                    </td>
                    <td>
                      Rs. {payment.amount}
                    </td>
                    <td>
                      {payment.payment_method}
                    </td>
                    <td>
                      {payment.reference_number ||
                        "-"}
                    </td>
                    <td>
                      {payment.notes || "-"}
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

export default Payments;
