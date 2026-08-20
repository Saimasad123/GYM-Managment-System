import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";

import { AuthProvider, useAuth } from "./context/AuthContext";
import AdminLayout from "./layouts/AdminLayout";

import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Members from "./pages/Members";
import Memberships from "./pages/Memberships";
import MembershipPackages from "./pages/MembershipPackages";
import MembershipStatus from "./pages/MembershipStatus";
import Expenses from "./pages/Expenses";
import Payments from "./pages/Payments";
import Attendance from "./pages/Attendance";
import Trainers from "./pages/Trainers";
import Staff from "./pages/Staff";
import Reminders from "./pages/Reminders";
import FinancialReports from "./pages/FinancialReports";

function ProtectedRoute({ children }) {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div className="login-page">
        <div className="login-card" style={{ textAlign: "center" }}>
          <div className="login-logo" style={{ margin: "0 auto 16px" }}>GYM</div>
          <p style={{ color: "#6b7280" }}>Loading...</p>
        </div>
      </div>
    );
  }

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  return children;
}

function AppRoutes() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />

      <Route
        path="/"
        element={
          <ProtectedRoute>
            <AdminLayout />
          </ProtectedRoute>
        }
      >
        <Route index element={<Navigate to="/dashboard" replace />} />
        <Route path="dashboard" element={<Dashboard />} />
        <Route path="members" element={<Members />} />
        <Route path="memberships" element={<Memberships />} />
        <Route
          path="membership-packages"
          element={<MembershipPackages />}
        />
        <Route
          path="membership-status"
          element={<MembershipStatus />}
        />
        <Route path="payments" element={<Payments />} />
        <Route path="expenses" element={<Expenses />} />
        <Route path="attendance" element={<Attendance />} />
        <Route path="trainers" element={<Trainers />} />
        <Route path="staff" element={<Staff />} />
        <Route path="reminders" element={<Reminders />} />
        <Route path="financial-reports" element={<FinancialReports />} />
      </Route>

      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <AppRoutes />
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;
