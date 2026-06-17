import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { modelsApi } from '../lib/api';
import { Plus, Brain, Download, Zap, Star, Trash2, ExternalLink } from 'lucide-react';
import toast from 'react-hot-toast';

const FRAMEWORKS = ['pytorch', 'tensorflow', 'sklearn', 'onnx', 'huggingface', 'xgboost', 'custom'];
const TASKS = ['classification', 'regression', 'object_detection', 'nlp_classification', 'text_generation', 'anomaly_detection', 'custom'];

function CreateModelModal({ onClose }: { onClose: () => void }) {
  const qc = useQueryClient();
  const [form, setForm] = useState({
    name: '', description: '', framework: 'pytorch', task: 'classification',
    is_public: false, tags: '', license: '', readme: '',
  });
  const mut = useMutation({
    mutationFn: modelsApi.create,
    onSuccess: () => { qc.invalidateQueries({ queryKey: ['my-models'] }); toast.success('Model created!'); onClose(); },
    onError: () => toast.error('Failed to create model'),
  });
  const s = (f: string) => (e: any) => setForm(p => ({ ...p, [f]: e.target.type === 'checkbox' ? e.target.checked : e.target.value }));
  return (
    <div className="fixed inset-0 bg-black/60 flex items-center justify-center z-50 p-4">
      <div className="bg-gray-900 border border-gray-800 rounded-2xl w-full max-w-lg p-6">
        <h2 className="text-white font-semibold text-lg mb-5">New Model</h2>
        <div className="space-y-4">
          <div>
            <label className="text-sm text-gray-400">Name *</label>
            <input value={form.name} onChange={s('name')} className="mt-1 w-full bg-gray-800 border border-gray-700 text-white rounded-lg px-3 py-2 focus:outline-none focus:border-violet-500" placeholder="My Awesome Model" />
          </div>
          <div>
            <label className="text-sm text-gray-400">Description</label>
            <textarea value={form.description} onChange={s('description')} rows={2} className="mt-1 w-full bg-gray-800 border border-gray-700 text-white rounded-lg px-3 py-2 focus:outline-none focus:border-violet-500 resize-none" />
          </div>
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="text-sm text-gray-400">Framework</label>
              <select value={form.framework} onChange={s('framework')} className="mt-1 w-full bg-gray-800 border border-gray-700 text-white rounded-lg px-3 py-2">
                {FRAMEWORKS.map(f => <option key={f}>{f}</option>)}
              </select>
            </div>
            <div>
              <label className="text-sm text-gray-400">Task</label>
              <select value={form.task} onChange={s('task')} className="mt-1 w-full bg-gray-800 border border-gray-700 text-white rounded-lg px-3 py-2">
                {TASKS.map(t => <option key={t}>{t}</option>)}
              </select>
            </div>
          </div>
          <label className="flex items-center gap-2 cursor-pointer">
            <input type="checkbox" checked={form.is_public} onChange={s('is_public')} className="accent-violet-500" />
            <span className="text-sm text-gray-400">Make public</span>
          </label>
        </div>
        <div className="flex gap-3 mt-6">
          <button onClick={onClose} className="flex-1 bg-gray-800 text-gray-300 rounded-lg py-2 hover:bg-gray-700">Cancel</button>
          <button onClick={() => mut.mutate({ ...form, tags: form.tags.split(',').map(t => t.trim()).filter(Boolean) })} disabled={!form.name || mut.isPending}
            className="flex-1 bg-violet-600 text-white rounded-lg py-2 hover:bg-violet-700 disabled:opacity-50">
            {mut.isPending ? 'Creating...' : 'Create'}
          </button>
        </div>
      </div>
    </div>
  );
}

export default function ModelsPage() {
  const [showCreate, setShowCreate] = useState(false);
  const qc = useQueryClient();
  const { data: models = [], isLoading } = useQuery({ queryKey: ['my-models'], queryFn: modelsApi.listMy });
  const deleteMut = useMutation({
    mutationFn: modelsApi.delete,
    onSuccess: () => { qc.invalidateQueries({ queryKey: ['my-models'] }); toast.success('Model deleted'); },
  });

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Model Registry</h1>
          <p className="text-gray-400 mt-1">Manage and version your ML models</p>
        </div>
        <button onClick={() => setShowCreate(true)} className="flex items-center gap-2 bg-violet-600 hover:bg-violet-700 text-white px-4 py-2 rounded-lg transition">
          <Plus size={16} /> New Model
        </button>
      </div>

      {isLoading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {[...Array(6)].map((_, i) => <div key={i} className="bg-gray-900 border border-gray-800 rounded-xl h-40 animate-pulse" />)}
        </div>
      ) : models.length === 0 ? (
        <div className="text-center py-20">
          <Brain size={40} className="text-gray-700 mx-auto mb-4" />
          <p className="text-gray-400 font-medium">No models yet</p>
          <p className="text-gray-600 text-sm mt-1">Upload your first ML model to get started</p>
          <button onClick={() => setShowCreate(true)} className="mt-4 bg-violet-600 text-white px-5 py-2 rounded-lg hover:bg-violet-700">
            Create Model
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {models.map((m: any) => (
            <div key={m.id} className="bg-gray-900 border border-gray-800 rounded-xl p-5 hover:border-gray-700 transition group">
              <div className="flex items-start justify-between mb-3">
                <div className="flex-1 min-w-0">
                  <h3 className="text-white font-medium truncate">{m.name}</h3>
                  <p className="text-gray-500 text-xs mt-0.5">{m.framework} · {m.task}</p>
                </div>
                <span className={`ml-2 text-xs px-2 py-0.5 rounded-full shrink-0 ${
                  m.status === 'active' ? 'bg-emerald-900/50 text-emerald-400' : 'bg-gray-800 text-gray-500'
                }`}>{m.status}</span>
              </div>
              {m.description && <p className="text-gray-400 text-sm line-clamp-2 mb-3">{m.description}</p>}
              {m.tags?.length > 0 && (
                <div className="flex flex-wrap gap-1 mb-3">
                  {m.tags.map((t: string) => <span key={t} className="text-xs bg-gray-800 text-gray-400 px-2 py-0.5 rounded">{t}</span>)}
                </div>
              )}
              <div className="flex items-center gap-4 text-xs text-gray-600 mt-auto pt-3 border-t border-gray-800">
                <span className="flex items-center gap-1"><Download size={11} />{m.download_count}</span>
                <span className="flex items-center gap-1"><Zap size={11} />{m.inference_count}</span>
                <span className="flex items-center gap-1"><Star size={11} />{m.star_count}</span>
                <div className="ml-auto opacity-0 group-hover:opacity-100 transition">
                  <button onClick={() => deleteMut.mutate(m.id)} className="text-red-500 hover:text-red-400">
                    <Trash2 size={14} />
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {showCreate && <CreateModelModal onClose={() => setShowCreate(false)} />}
    </div>
  );
}
