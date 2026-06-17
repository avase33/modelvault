import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { trainingApi } from '../lib/api';
import { Plus, Activity, Clock, CheckCircle, XCircle, AlertCircle, StopCircle } from 'lucide-react';
import { formatDistanceToNow } from 'date-fns';
import toast from 'react-hot-toast';

const STATUS_CONFIG: Record<string, any> = {
  queued: { color: 'bg-yellow-900/50 text-yellow-400', icon: Clock },
  running: { color: 'bg-blue-900/50 text-blue-400', icon: Activity },
  completed: { color: 'bg-emerald-900/50 text-emerald-400', icon: CheckCircle },
  failed: { color: 'bg-red-900/50 text-red-400', icon: XCircle },
  cancelled: { color: 'bg-gray-800 text-gray-500', icon: AlertCircle },
};

function CreateJobModal({ onClose }: { onClose: () => void }) {
  const qc = useQueryClient();
  const [form, setForm] = useState({ name: '', framework: 'pytorch', compute_type: 'cpu', max_epochs: 100 });
  const mut = useMutation({
    mutationFn: trainingApi.create,
    onSuccess: () => { qc.invalidateQueries({ queryKey: ['jobs'] }); toast.success('Job queued!'); onClose(); },
    onError: () => toast.error('Failed to create job'),
  });
  const s = (f: string) => (e: any) => setForm(p => ({ ...p, [f]: e.target.value }));
  return (
    <div className="fixed inset-0 bg-black/60 flex items-center justify-center z-50 p-4">
      <div className="bg-gray-900 border border-gray-800 rounded-2xl w-full max-w-md p-6">
        <h2 className="text-white font-semibold text-lg mb-5">New Training Job</h2>
        <div className="space-y-4">
          <div>
            <label className="text-sm text-gray-400">Job Name *</label>
            <input value={form.name} onChange={s('name')} className="mt-1 w-full bg-gray-800 border border-gray-700 text-white rounded-lg px-3 py-2 focus:outline-none focus:border-violet-500" placeholder="ResNet50-v2 training" />
          </div>
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="text-sm text-gray-400">Framework</label>
              <select value={form.framework} onChange={s('framework')} className="mt-1 w-full bg-gray-800 border border-gray-700 text-white rounded-lg px-3 py-2">
                {['pytorch', 'tensorflow', 'sklearn', 'xgboost'].map(f => <option key={f}>{f}</option>)}
              </select>
            </div>
            <div>
              <label className="text-sm text-gray-400">Compute</label>
              <select value={form.compute_type} onChange={s('compute_type')} className="mt-1 w-full bg-gray-800 border border-gray-700 text-white rounded-lg px-3 py-2">
                {['cpu', 'gpu_t4', 'gpu_a100', 'gpu_v100'].map(c => <option key={c}>{c}</option>)}
              </select>
            </div>
          </div>
          <div>
            <label className="text-sm text-gray-400">Max Epochs</label>
            <input type="number" value={form.max_epochs} onChange={s('max_epochs')} className="mt-1 w-full bg-gray-800 border border-gray-700 text-white rounded-lg px-3 py-2" />
          </div>
        </div>
        <div className="flex gap-3 mt-6">
          <button onClick={onClose} className="flex-1 bg-gray-800 text-gray-300 rounded-lg py-2 hover:bg-gray-700">Cancel</button>
          <button onClick={() => mut.mutate(form)} disabled={!form.name || mut.isPending}
            className="flex-1 bg-violet-600 text-white rounded-lg py-2 hover:bg-violet-700 disabled:opacity-50">
            {mut.isPending ? 'Queueing...' : 'Queue Job'}
          </button>
        </div>
      </div>
    </div>
  );
}

export default function TrainingPage() {
  const [showCreate, setShowCreate] = useState(false);
  const qc = useQueryClient();
  const { data: jobs = [], isLoading } = useQuery({ queryKey: ['jobs'], queryFn: () => trainingApi.list(), refetchInterval: 5000 });
  const cancelMut = useMutation({
    mutationFn: trainingApi.cancel,
    onSuccess: () => { qc.invalidateQueries({ queryKey: ['jobs'] }); toast.success('Job cancelled'); },
  });

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Training Jobs</h1>
          <p className="text-gray-400 mt-1">Monitor and manage training runs</p>
        </div>
        <button onClick={() => setShowCreate(true)} className="flex items-center gap-2 bg-violet-600 hover:bg-violet-700 text-white px-4 py-2 rounded-lg">
          <Plus size={16} /> New Job
        </button>
      </div>

      {isLoading ? (
        <div className="space-y-3">{[...Array(4)].map((_, i) => <div key={i} className="bg-gray-900 border border-gray-800 rounded-xl h-20 animate-pulse" />)}</div>
      ) : jobs.length === 0 ? (
        <div className="text-center py-20">
          <Activity size={40} className="text-gray-700 mx-auto mb-4" />
          <p className="text-gray-400 font-medium">No training jobs yet</p>
          <button onClick={() => setShowCreate(true)} className="mt-4 bg-violet-600 text-white px-5 py-2 rounded-lg hover:bg-violet-700">Launch First Job</button>
        </div>
      ) : (
        <div className="space-y-3">
          {jobs.map((j: any) => {
            const cfg = STATUS_CONFIG[j.status] || STATUS_CONFIG.cancelled;
            const Icon = cfg.icon;
            return (
              <div key={j.id} className="bg-gray-900 border border-gray-800 rounded-xl p-5">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <Icon size={18} className={cfg.color.split(' ')[1]} />
                    <div>
                      <h3 className="text-white font-medium">{j.name}</h3>
                      <p className="text-gray-500 text-xs">{j.framework} · {j.compute_type} · Queued {formatDistanceToNow(new Date(j.queued_at), { addSuffix: true })}</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    <span className={`text-xs px-2.5 py-1 rounded-full ${cfg.color}`}>{j.status}</span>
                    {(j.status === 'running' || j.status === 'queued') && (
                      <button onClick={() => cancelMut.mutate(j.id)} className="text-gray-500 hover:text-red-400 transition">
                        <StopCircle size={16} />
                      </button>
                    )}
                  </div>
                </div>
                {j.status === 'running' && (
                  <div className="mt-3">
                    <div className="flex justify-between text-xs text-gray-500 mb-1">
                      <span>Epoch {j.current_epoch} / {j.max_epochs || '?'}</span>
                      <span>{j.progress_percent?.toFixed(1)}%</span>
                    </div>
                    <div className="bg-gray-800 rounded-full h-1.5">
                      <div className="bg-violet-500 h-1.5 rounded-full transition-all" style={{ width: `${j.progress_percent}%` }} />
                    </div>
                  </div>
                )}
                {j.final_metrics && Object.keys(j.final_metrics).length > 0 && (
                  <div className="mt-3 flex gap-4">
                    {Object.entries(j.final_metrics).slice(0, 4).map(([k, v]) => (
                      <div key={k} className="text-xs">
                        <span className="text-gray-500">{k}: </span>
                        <span className="text-white">{typeof v === 'number' ? v.toFixed(4) : String(v)}</span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
      {showCreate && <CreateJobModal onClose={() => setShowCreate(false)} />}
    </div>
  );
}
