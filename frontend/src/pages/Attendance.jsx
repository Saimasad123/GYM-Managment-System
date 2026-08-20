import { useEffect, useMemo, useState } from "react";
import api, { clearCacheFor } from "../services/api";

const STATUS_OPTIONS = [
  { value: "present", label: "Present" },
  { value: "absent", label: "Absent" },
  { value: "late", label: "Late" },
];

function Attendance() {
  const today = new Date();
  const [selectedYear, setSelectedYear] = useState(
    today.getFullYear()
  );
  const [selectedMonth, setSelectedMonth] = useState(
    today.getMonth() + 1
  );
  const [selectedDay, setSelectedDay] = useState(
    today.getDate()
  );

  const [members, setMembers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const selectedDate = useMemo(() => {
    const year = Number(selectedYear);
    const month = Number(selectedMonth);
    const day = Number(selectedDay);

    if (!year || !month || !day) return null;

    const date = new Date(year, month - 1, day);

    if (
      date.getFullYear() !== year ||
      date.getMonth() !== month - 1 ||
      date.getDate() !== day
    ) {
      return null;
    }

    return `${year}-${String(month).padStart(2, "0")}-${String(day).padStart(2, "0")}`;
  }, [selectedYear, selectedMonth, selectedDay]);

  const daysInMonth = useMemo(() => {
    const year = Number(selectedYear);
    const month = Number(selectedMonth);

    if (!year || !month) return 31;

    return new Date(year, month, 0).getDate();
  }, [selectedYear, selectedMonth]);

  const currentYear = new Date().getFullYear();
  const yearOptions = useMemo(
    () =>
      Array.from({ length: 11 }, (_, i) => currentYear - 5 + i),
    [currentYear]
  );

  const loadAttendance = async () => {
    if (!selectedDate) return;

    try {
      setLoading(true);
      setError("");

      const response = await api.get(
        "/attendance/members",
        {
          params: { date: selectedDate },
        }
      );

      setMembers(response.data || []);
    } catch (err) {
      console.error(err);
      setError(
        err.response?.data?.detail ||
          "Unable to load attendance."
      );
      setMembers([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAttendance();
  }, [selectedDate]);

  const handleYearChange = (value) => {
    setSelectedYear(Number(value));
  };

  const handleMonthChange = (value) => {
    const month = Number(value);
    setSelectedMonth(month);

    const maxDay = new Date(
      Number(selectedYear),
      month,
      0
    ).getDate();

    if (Number(selectedDay) > maxDay) {
      setSelectedDay(maxDay);
    }
  };

  const handleDayChange = (value) => {
    setSelectedDay(Number(value));
  };

  const handleStatusChange = (memberId, status) => {
    setMembers((prev) =>
      prev.map((member) =>
        member.member_id === memberId
          ? { ...member, status }
          : member
      )
    );
  };

  const handleSaveAll = async () => {
    if (!selectedDate) {
      setError("Please select a valid date first.");
      return;
    }

    setError("");
    setSuccess("");

    try {
      setSaving(true);

      const promises = [];
      const updates = [];
      const creates = [];

      for (const member of members) {
        if (!member.status) continue;

        if (member.attendance_id) {
          updates.push(
            api
              .patch(`/attendance/${member.attendance_id}`, {
                status: member.status,
              })
              .catch((err) => ({
                member_id: member.member_id,
                error: err,
              }))
          );
        } else {
          creates.push(
            api
              .post("/attendance", {
                member_id: member.member_id,
                attendance_date: selectedDate,
                status: member.status,
              })
              .catch((err) => ({
                member_id: member.member_id,
                error: err,
              }))
          );
        }
      }

      if (updates.length === 0 && creates.length === 0) {
        setError("Please mark at least one attendance status before saving.");
        setSaving(false);
        return;
      }

      const results = await Promise.all([
        ...updates,
        ...creates,
      ]);

      const failures = results.filter(
        (result) => result && result.error
      );

      if (failures.length > 0) {
        console.error("Some saves failed:", failures);
        setError(
          `Saved with errors. ${failures.length} record(s) failed.`
        );
      } else {
        setSuccess("Attendance saved successfully.");
      }

      clearCacheFor("/attendance/members");
      await loadAttendance();
    } catch (err) {
      console.error(err);
      setError(
        err.response?.data?.detail ||
          "Unable to save attendance."
      );
    } finally {
      setSaving(false);
    }
  };

  const getStatusBadge = (status) => {
    if (!status) {
      return (
        <span
          style={{
            display: "inline-block",
            padding: "4px 10px",
            borderRadius: "9999px",
            background: "#f3f4f6",
            color: "#6b7280",
            fontSize: "12px",
            fontWeight: 600,
          }}
        >
          Not Marked
        </span>
      );
    }

    switch (status) {
      case "present":
        return (
          <span className="status-active">
            Present
          </span>
        );
      case "absent":
        return (
          <span className="status-inactive">
            Absent
          </span>
        );
      case "late":
        return (
          <span className="status-warning">
            Late
          </span>
        );
      default:
        return status;
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return "-";
    const date = new Date(dateString + "T00:00:00");
    return date.toLocaleDateString("en-US", {
      weekday: "short",
      year: "numeric",
      month: "long",
      day: "numeric",
    });
  };

  const markedCount = members.filter(
    (m) => m.status
  ).length;

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h1>Attendance</h1>
          <p>
            Select a date to view and mark member
            attendance.
          </p>
        </div>
      </div>

      {error && (
        <div className="error-message">{error}</div>
      )}
      {success && (
        <div className="success-message">{success}</div>
      )}

      <div className="form-card">
        <h2>Select Date</h2>
        <div className="form-grid">
          <div className="form-group">
            <label>Year</label>
            <select
              value={selectedYear}
              onChange={(e) =>
                handleYearChange(e.target.value)
              }
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
          </div>
          <div className="form-group">
            <label>Month</label>
            <select
              value={selectedMonth}
              onChange={(e) =>
                handleMonthChange(e.target.value)
              }
            >
              {Array.from({ length: 12 }, (_, i) => (
                <option
                  key={i + 1}
                  value={i + 1}
                >
                  {new Date(
                    Number(selectedYear),
                    i,
                    1
                  ).toLocaleString(
                    "default",
                    { month: "long" }
                  )}
                </option>
              ))}
            </select>
          </div>
          <div className="form-group">
            <label>Date</label>
            <select
              value={selectedDay || ""}
              onChange={(e) =>
                handleDayChange(e.target.value)
              }
            >
              <option value="">
                Select day
              </option>
              {Array.from(
                { length: daysInMonth },
                (_, i) => i + 1
              ).map((day) => (
                <option
                  key={day}
                  value={day}
                >
                  {day}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {selectedDate && (
        <div className="dashboard-section">
          <div className="table-header">
            <h2>
              Attendance for{" "}
              {formatDate(selectedDate)}{" "}
              <span style={{ fontWeight: 400, fontSize: "14px", color: "#6b7280" }}>
                ({markedCount}/{members.length} marked)
              </span>
            </h2>
            <button
              className="primary-button"
              onClick={handleSaveAll}
              disabled={saving || loading}
            >
              {saving
                ? "Saving..."
                : "Save Attendance"}
            </button>
          </div>

          {loading ? (
            <p>Loading attendance...</p>
          ) : members.length === 0 ? (
            <p>No active members found.</p>
          ) : (
            <div className="table-container">
              <table>
                <thead>
                  <tr>
                    <th>Member</th>
                    <th>Code</th>
                    <th>Status</th>
                    <th>Check In</th>
                    <th>Check Out</th>
                  </tr>
                </thead>
                <tbody>
                  {members.map((member) => (
                    <tr key={member.member_id}>
                      <td>
                        {member.member_name ||
                          `Member #${member.member_id}`}
                      </td>
                      <td>
                        {member.member_code}
                      </td>
                      <td>
                        <select
                          value={
                            member.status || ""
                          }
                          onChange={(e) =>
                            handleStatusChange(
                              member.member_id,
                              e.target.value
                            )
                          }
                          style={{
                            padding: "6px 10px",
                            border: "1px solid #d1d5db",
                            borderRadius: "6px",
                            minWidth: "120px",
                          }}
                        >
                          <option value="">
                            Not Marked
                          </option>
                          {STATUS_OPTIONS.map(
                            (opt) => (
                              <option
                                key={
                                  opt.value
                                }
                                value={
                                  opt.value
                                }
                              >
                                {opt.label}
                              </option>
                            )
                          )}
                        </select>
                      </td>
                      <td>
                        {member.check_in || "-"}
                      </td>
                      <td>
                        {member.check_out || "-"}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default Attendance;
