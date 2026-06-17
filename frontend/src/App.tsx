import { useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Toaster } from 'react-hot-toast';
import { useAuthStore } from './store/auth';
import Layout from './components/Layout';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import DashboardPage from './pages/DashboardPage';
import ModelsPage from './pages/ModelsPage';
import DatasetsPage from './pages/DatasetsPage';
import TrainingPage from './pages/TrainingPage';
import ApiKeysPage from './pages/ApiKeysPage';

const queryClient = new QueryClient({
  defaultOptions: { queries: { retry: 1, staleTime: 30_000 } },
});

function PrivateRoute({ children }: { children: JSX.Element }) {
  const user = useAuthStore(s => s.user);
  const token = localStorage.getItem('access_token');
  if (!token && !user) return <Navigate to="/login" replace />;
  return children;
}

function AppInit() {
  const fetchMe = useAuthStore(s => s.fetchMe);
  useEffect(() => { fetchMe(); }, [fetchMe]);
  return null;
}

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <AppInit />
        <Toaster
          position="top-right"
          toastOptions={{
            style: { background: '#1f2937', color: '#f9fafb', border: '1px solid #374151' },
          }}
        />
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/" element={<PrivateRoute><Layout /></PrivateRoute>}>
            <Route index element={<Navigate to="/dashboard" replace />} />
            <Route path="dashboard" element={<DashboardPage />} />
            <Route path="models" element={<ModelsPage />} />
            <Route path="datasets" element={<DatasetsPage />} />
            <Route path="training" element={<TrainingPage />} />
            <Route path="api-keys" element={<ApiKeysPage />} />
          </Route>
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
}
