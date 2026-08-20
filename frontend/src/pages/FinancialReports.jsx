import { useEffect, useState } from "react";
import api from "../services/api";

function FinancialReports() {
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const loadReport = async () => {
      try {
        setLoading(true);
        setError("");

        const response = await api.get(
          "/dashboard/summary"
        );
        setSummary(response.data);
      } catch (err) {
        console.error(err);
        setError(
          err.response?.data?.detail ||
            "Unable to load financial reports."
        );
      } finally {
        setLoading(false);
      }
    };

    loadReport();
  }, []);

  if (loading) {
    return (
      <div className="page">
        <div className="page-header">
          <div>
            <h1>Financial Reports</h1>
            <p>
              View revenue, expenses and profit
              reports.
            </p>
          </div>
        </div>
        <p>Loading reports...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="page">
        <div className="page-header">
          <div>
            <h1>Financial Reports</h1>
            <p>
              View revenue, expenses and profit
              reports.
            </p>
          </div>
        </div>
        <div className="error-message">
          {error}
        </div>
      </div>
    );
  }

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h1>Financial Reports</h1>
          <p>
            View revenue, expenses and profit
            reports.
          </p>
        </div>
      </div>

      <div className="dashboard-grid">
        <div className="dashboard-card">
          <span>Monthly Revenue</span>
          <strong>
            Rs. {summary?.monthly_revenue ?? 0}
          </strong>
        </div>
        <div className="dashboard-card">
          <span>Monthly Expenses</span>
          <strong>
            Rs. {summary?.monthly_expenses ?? 0}
          </strong>
        </div>
        <div className="dashboard-card">
          <span>Monthly Profit</span>
          <strong>
            Rs. {summary?.monthly_profit ?? 0}
          </strong>
        </div>
        <div className="dashboard-card">
          <span>Annual Revenue</span>
          <strong>
            Rs. {summary?.annual_revenue ?? 0}
          </strong>
        </div>
        <div className="dashboard-card">
          <span>Annual Expenses</span>
          <strong>
            Rs. {summary?.annual_expenses ?? 0}
          </strong>
        </div>
        <div className="dashboard-card">
          <span>Annual Profit</span>
          <strong>
            Rs. {summary?.annual_profit ?? 0}
          </strong>
        </div>
      </div>

      <div className="dashboard-section">
        <h2>Daily Financial Report</h2>
        {summary?.daily_financials?.length ? (
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Revenue</th>
                  <th>Expenses</th>
                  <th>Profit</th>
                </tr>
              </thead>
              <tbody>
                {summary.daily_financials.map(
                  (item) => (
                    <tr key={item.date}>
                      <td>
                        {new Date(
                          item.date
                        ).toLocaleDateString()}
                      </td>
                      <td>
                        Rs. {item.revenue}
                      </td>
                      <td>
                        Rs. {item.expenses}
                      </td>
                      <td>
                        Rs. {item.profit}
                      </td>
                    </tr>
                  )
                )}
              </tbody>
            </table>
          </div>
        ) : (
          <p>No financial records available.</p>
        )}
      </div>
    </div>
  );
}

export default FinancialReports;
