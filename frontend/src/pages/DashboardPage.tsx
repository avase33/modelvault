import { useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import { modelsApi, datasetsApi, trainingApi } from '../lib/api';
import { useAuthStore } from '../store/auth';
import {
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer
} from 'recharts';
import { Brain, Database, Activity, Key, TrendingUp, Clock } from 'lucide-react';

const mockInferenceData = Array.from({ length: 14 }, (_, i) => ({
  date: `Jun ${i + 4}`,
  calls: Math.floor(Math.random() * 5000) + 1000,
}));

function StatCard({ icon: Icon, label, value, sub, color }: any) {
  return (
    <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
      <div className="flex items-center justify-between mb-3">
        <span className="text-gray-400 text-sm">{label}</span>
        <div className={`w-8 h-8 rounded-lg ${color} flex items-center justify-center`}>
          <Icon size={16} className="text-white" />
        </div>
      </div>
      <div className="text-2xl font-bold text-white">{value}</div>
      {sub && <div className="text-xs text-gray-500 mt-1">{sub}</div>}
    </div>
  );
}

export default function DashboardPage() {
  const user = useAuthStore(s => s.user);
  const { data: models = [] } = useQuery({ queryKey: ['my-models'], queryFn: modelsApi.listMy });
  const { data: datasets = [] } = useQuery({ queryKey: ['my-datasets'], queryFn: datasetsApi.listMy });
  const { data: jobs = [] } = useQuery({ queryKey: ['my-jobs'], queryFn: () => trainingApi.list() });

  const activeJobs = jobs.filter((j: any) => j.status === 'running' || j.status === 'queued');

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">
          Good morning, {user?.full_name?.split(' ')[0] || user?.username} 👋
        </h1>
        <p className="text-gray-400 mt-1">Here's what's happening with your ML projects.</p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard icon={Brain} label="Models" value={models.length} sub="in registry" color="bg-violet-600" />
        <StatCard icon={Database} label="Datasets" value={datasets.length} sub="uploaded" color="bg-blue-600" />
        <StatCard icon={Activity} label="Active Jobs" value={activeJobs.length} sub="running now" color="bg-emerald-600" />
        <StatCard icon={TrendingUp} label="Inferences" value="24.3k" sub="this month" color="bg-orange-600" />
      </div>

      {/* Chart */}
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
        <h2 className="text-white font-semibold mb-4">API Inference Calls (last 14 days)</h2>
        <ResponsiveContainer width="100%" height={220}>
          <AreaChart data={mockInferenceData}>
            <defs>
              <linearGradient id="grad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#7c3aed" stopOpacity={0.3} />
                <stop offset="95%" stopColor="#7c3aed" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#1f2937" />
            <XAxis dataKey="date" tick={{ fill: '#6b7280', fontSize: 12 }} />
            <YAxis tick={{ fill: '#6b7280', fontSize: 12 }} />
            <Tooltip
              contentStyle={{ background: '#111827', border: '1px solid #374151', borderRadius: 8 }}
              labelStyle={{ color: '#f9fafb' }}
            />
            <Area type="monotone" dataKey="calls" stroke="#7c3aed" fill="url(#grad)" strokeWidth={2} />
          </AreaChart>
        </ResponsiveContainer>
      </div>

      {/* Recent Models & Jobs */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Models */}
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
          <h2 className="text-white font-semibold mb-4 flex items-center gap-2">
            <Brain size={16} className="text-violet-400" /> Recent Models
          </h2>
          {models.length === 0 ? (
            <p className="text-gray-500 text-sm">No models yet. Upload your first model!</p>
          ) : (
            <div className="space-y-3">
              {models.slice(0, 5).map((m: any) => (
                <div key={m.id} className="flex items-center justify-between py-2 border-b border-gray-800 last:border-0">
                  <div>
                    <p className="text-white text-sm font-medium">{m.name}</p>
                    <p className="text-gray-500 text-xs">{m.framework} · {m.task}</p>
                  </div>
                  <span className={`text-xs px-2 py-0.5 rounded-full ${
                    m.status === 'active' ? 'bg-emerald-900 text-emerald-400' :
                    m.status === 'draft' ? 'bg-gray-800 text-gray-400' : 'bg-gray-800 text-gray-400'
                  }`}>{m.status}</span>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Recent Jobs */}
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
          <h2 className="text-white font-semibold mb-4 flex items-center gap-2">
            <Clock size={16} className="text-blue-400" /> Training Jobs
          </h2>
          {jobs.length === 0 ? (
            <p className="text-gray-500 text-sm">No training jobs yet.</p>
          ) : (
            <div className="space-y-3">
              {jobs.slice(0, 5).map((j: any) => (
                <div key={j.id} className="flex items-center justify-between py-2 border-b border-gray-800 last:border-0">
                  <div>
                    <p className="text-white text-sm font-medium">{j.name}</p>
                    <p className="text-gray-500 text-xs">{j.framework} · {j.compute_type}</p>
                  </div>
                  <div className="text-right">
                    <span className={`text-xs px-2 py-0.5 rounded-full ${
                      j.status === 'running' ? 'bg-blue-900 text-blue-400' :
                      j.status === 'completed' ? 'bg-emerald-900 text-emerald-400' :
                      j.status === 'failed' ? 'bg-red-900 text-red-400' : 'bg-gray-800 text-gray-400'
                    }`}>{j.status}</span>
                    {j.status === 'running' && (
                      <div className="mt-1 w-20 bg-gray-800 rounded-full h-1">
                        <div
                          className="bg-blue-500 h-1 rounded-full transition-all"
                          style={{ width: `${j.progress_percent}%` }}
                        />
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
