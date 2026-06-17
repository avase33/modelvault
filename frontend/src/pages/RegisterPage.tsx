import { useState, FormEvent } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuthStore } from '../store/auth';
import toast from 'react-hot-toast';

export default function RegisterPage() {
  const navigate = useNavigate();
  const { register, isLoading } = useAuthStore();
  const [form, setForm] = useState({ email: '', username: '', full_name: '', password: '' });

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    try {
      await register(form);
      toast.success('Account created!');
      navigate('/dashboard');
    } catch (err: any) {
      toast.error(err.response?.data?.detail || 'Registration failed');
    }
  };

  const set = (field: string) => (e: any) =>
    setForm(prev => ({ ...prev, [field]: e.target.value }));

  return (
    <div className="min-h-screen bg-gray-950 flex items-center justify-center px-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <div className="inline-flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-violet-600 flex items-center justify-center">
              <span className="text-white font-bold text-lg">M</span>
            </div>
            <span className="text-white text-2xl font-bold">ModelVault</span>
          </div>
          <p className="text-gray-400 mt-2">Start managing your AI models today</p>
        </div>

        <div className="bg-gray-900 border border-gray-800 rounded-2xl p-8">
          <h1 className="text-white text-xl font-semibold mb-6">Create your account</h1>
          <form onSubmit={handleSubmit} className="space-y-4">
            {[
              { label: 'Full Name', field: 'full_name', type: 'text', placeholder: 'Jane Smith' },
              { label: 'Username', field: 'username', type: 'text', placeholder: 'janesmith' },
              { label: 'Email', field: 'email', type: 'email', placeholder: 'jane@company.com' },
              { label: 'Password', field: 'password', type: 'password', placeholder: '••••••••' },
            ].map(({ label, field, type, placeholder }) => (
              <div key={field}>
                <label className="block text-sm text-gray-400 mb-1.5">{label}</label>
                <input
                  type={type}
                  value={(form as any)[field]}
                  onChange={set(field)}
                  required
                  className="w-full bg-gray-800 border border-gray-700 text-white rounded-lg px-4 py-2.5 focus:outline-none focus:border-violet-500 transition"
                  placeholder={placeholder}
                />
              </div>
            ))}
            <button
              type="submit"
              disabled={isLoading}
              className="w-full bg-violet-600 hover:bg-violet-700 disabled:opacity-50 text-white font-medium rounded-lg py-2.5 transition mt-2"
            >
              {isLoading ? 'Creating account...' : 'Create account'}
            </button>
          </form>
          <p className="text-center text-gray-500 text-sm mt-6">
            Already have an account?{' '}
            <Link to="/login" className="text-violet-400 hover:text-violet-300">
              Sign in
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
