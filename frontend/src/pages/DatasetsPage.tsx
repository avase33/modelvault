import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { datasetsApi } from '../lib/api';
import { Plus, Database, Trash2, Upload } from 'lucide-react';
import toast from 'react-hot-toast';

const TYPES = ['tabular', 'image', 'text', 'audio', 'video', 'time_series', 'multimodal'];

function CreateDatasetModal({ onClose }: { onClose: () => void }) {
  const qc = useQueryClient();
  const [form, setForm] = useState({ name: '', description: '', dataset_type: 'tabular', is_public: false });
  const mut = useMutation({
    mutationFn: datasetsApi.create,
    onSuccess: () => { qc.invalidateQueries({ queryKey: ['my-datasets'] }); toast.success('Dataset created!'); onClose(); },
    onError: () => toast.error('Failed to create dataset'),
  });
  const s = (f: string) => (e: any) => setForm(p => ({ ...p, [f]: e.target.type === 'checkbox' ? e.target.checked : e.target.value }));
  return (
    <div className="fixed inset-0 bg-black/60 flex items-center justify-center z-50 p-4">
      <div className="bg-gray-900 border border-gray-800 rounded-2xl w-full max-w-md p-6">
        <h2 className="text-white font-semibold text-lg mb-5">New Dataset</h2>
        <div className="space-y-4">
          <div>
            <label className="text-sm text-gray-400">Name *</label>
            <input value={form.name} onChange={s('name')} className="mt-1 w-full bg-gray-800 border border-gray-700 text-white rounded-lg px-3 py-2 focus:outline-none focus:border-violet-500" placeholder="ImageNet Subset" />
          </div>
          <div>
            <label className="text-sm text-gray-400">Description</label>
            <textarea value={form.description} onChange={s('description')} rows={2} className="mt-1 w-full bg-gray-800 border border-gray-700 text-white rounded-lg px-3 py-2 focus:outline-none focus:border-violet-500 resize-none" />
          </div>
          <div>
            <label className="text-sm text-gray-400">Type</label>
            <select value={form.dataset_type} onChange={s('dataset_type')} className="mt-1 w-full bg-gray-800 border border-gray-700 text-white rounded-lg px-3 py-2">
              {TYPES.map(t => <option key={t}>{t}</option>)}
            </select>
          </div>
          <label className="flex items-center gap-2 cursor-pointer">
            <input type="checkbox" checked={form.is_public} onChange={s('is_public')} className="accent-violet-500" />
            <span className="text-sm text-gray-400">Make public</span>
          </label>
        </div>
        <div className="flex gap-3 mt-6">
          <button onClick={onClose} className="flex-1 bg-gray-800 text-gray-300 rounded-lg py-2 hover:bg-gray-700">Cancel</button>
          <button onClick={() => mut.mutate(form)} disabled={!form.name || mut.isPending}
            className="flex-1 bg-violet-600 text-white rounded-lg py-2 hover:bg-violet-700 disabled:opacity-50">
            {mut.isPending ? 'Creating...' : 'Create'}
          </button>
        </div>
      </div>
    </div>
  );
}

function formatBytes(bytes?: number) {
  if (!bytes) return 'N/A';
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  if (bytes < 1024 ** 3) return `${(bytes / 1024 ** 2).toFixed(1)} MB`;
  return `${(bytes / 1024 ** 3).toFixed(1)} GB`;
}

export default function DatasetsPage() {
  const [showCreate, setShowCreate] = useState(false);
  const qc = useQueryClient();
  const { data: datasets = [], isLoading } = useQuery({ queryKey: ['my-datasets'], queryFn: datasetsApi.listMy });
  const deleteMut = useMutation({
    mutationFn: datasetsApi.delete,
    onSuccess: () => { qc.invalidateQueries({ queryKey: ['my-datasets'] }); toast.success('Dataset deleted'); },
  });

  const STATUS_COLOR: Record<string, string> = {
    ready: 'bg-emerald-900/50 text-emerald-400',
    uploading: 'bg-yellow-900/50 text-yellow-400',
    processing: 'bg-blue-900/50 text-blue-400',
    error: 'bg-red-900/50 text-red-400',
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Datasets</h1>
          <p className="text-gray-400 mt-1">Manage training data for your models</p>
        </div>
        <button onClick={() => setShowCreate(true)} className="flex items-center gap-2 bg-violet-600 hover:bg-violet-700 text-white px-4 py-2 rounded-lg">
          <Plus size={16} /> New Dataset
        </button>
      </div>

      {isLoading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {[...Array(6)].map((_, i) => <div key={i} className="bg-gray-900 border border-gray-800 rounded-xl h-36 animate-pulse" />)}
        </div>
      ) : datasets.length === 0 ? (
        <div className="text-center py-20">
          <Database size={40} className="text-gray-700 mx-auto mb-4" />
          <p className="text-gray-400 font-medium">No datasets yet</p>
          <p className="text-gray-600 text-sm mt-1">Upload your training data to get started</p>
          <button onClick={() => setShowCreate(true)} className="mt-4 bg-violet-600 text-white px-5 py-2 rounded-lg hover:bg-violet-700">Add Dataset</button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {datasets.map((d: any) => (
            <div key={d.id} className="bg-gray-900 border border-gray-800 rounded-xl p-5 hover:border-gray-700 transition group">
              <div className="flex items-start justify-between mb-2">
                <div>
                  <h3 className="text-white font-medium">{d.name}</h3>
                  <p className="text-gray-500 text-xs mt-0.5">{d.dataset_type}</p>
                </div>
                <span className={`text-xs px-2 py-0.5 rounded-full ${STATUS_COLOR[d.status] || 'bg-gray-800 text-gray-400'}`}>{d.status}</span>
              </div>
              {d.description && <p className="text-gray-400 text-sm line-clamp-2 mb-3">{d.description}</p>}
              <div className="grid grid-cols-3 gap-2 text-xs text-gray-500 py-3 border-t border-gray-800">
                <div><div className="text-white font-medium">{formatBytes(d.file_size_bytes)}</div><div>Size</div></div>
                <div><div className="text-white font-medium">{d.num_rows?.toLocaleString() || '—'}</div><div>Rows</div></div>
                <div><div className="text-white font-medium">{d.num_columns || '—'}</div><div>Cols</div></div>
              </div>
              <div className="flex justify-between items-center mt-2 opacity-0 group-hover:opacity-100 transition">
                <button className="flex items-center gap-1 text-xs text-gray-500 hover:text-violet-400">
                  <Upload size={12} /> Upload file
                </button>
                <button onClick={() => deleteMut.mutate(d.id)} className="text-red-500 hover:text-red-400">
                  <Trash2 size={14} />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
      {showCreate && <CreateDatasetModal onClose={() => setShowCreate(false)} />}
    </div>
  );
}
