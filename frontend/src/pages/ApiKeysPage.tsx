import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { authApi } from '../lib/api';
import { Key, Plus, Copy, Trash2, Eye, EyeOff } from 'lucide-react';
import toast from 'react-hot-toast';
import { formatDistanceToNow } from 'date-fns';

export default function ApiKeysPage() {
  const qc = useQueryClient();
  const [showCreate, setShowCreate] = useState(false);
  const [newKeyName, setNewKeyName] = useState('');
  const [createdKey, setCreatedKey] = useState<string | null>(null);
  const [showKey, setShowKey] = useState(false);

  const { data: keys = [] } = useQuery({ queryKey: ['api-keys'], queryFn: authApi.listApiKeys });

  const createMut = useMutation({
    mutationFn: authApi.createApiKey,
    onSuccess: (data) => {
      qc.invalidateQueries({ queryKey: ['api-keys'] });
      setCreatedKey(data.raw_key);
      setShowCreate(false);
      setNewKeyName('');
      toast.success('API key created!');
    },
  });

  const revokeMut = useMutation({
    mutationFn: authApi.revokeApiKey,
    onSuccess: () => { qc.invalidateQueries({ queryKey: ['api-keys'] }); toast.success('Key revoked'); },
  });

  const copy = (text: string) => { navigator.clipboard.writeText(text); toast.success('Copied!'); };

  return (
    <div className="space-y-6 max-w-3xl">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">API Keys</h1>
          <p className="text-gray-400 mt-1">Manage programmatic access to ModelVault</p>
        </div>
        <button onClick={() => setShowCreate(true)} className="flex items-center gap-2 bg-violet-600 hover:bg-violet-700 text-white px-4 py-2 rounded-lg">
          <Plus size={16} /> New Key
        </button>
      </div>

      {/* Newly created key alert */}
      {createdKey && (
        <div className="bg-emerald-900/20 border border-emerald-700 rounded-xl p-4">
          <p className="text-emerald-400 font-medium text-sm mb-2">⚡ Copy your new API key — it won't be shown again!</p>
          <div className="flex items-center gap-2">
            <code className="flex-1 bg-gray-900 text-emerald-300 px-3 py-2 rounded-lg text-sm font-mono overflow-hidden">
              {showKey ? createdKey : '•'.repeat(Math.min(createdKey.length, 40))}
            </code>
            <button onClick={() => setShowKey(s => !s)} className="text-gray-400 hover:text-white p-2">
              {showKey ? <EyeOff size={16} /> : <Eye size={16} />}
            </button>
            <button onClick={() => copy(createdKey)} className="text-gray-400 hover:text-white p-2"><Copy size={16} /></button>
          </div>
          <button onClick={() => setCreatedKey(null)} className="text-xs text-gray-500 mt-2 hover:text-gray-400">Dismiss</button>
        </div>
      )}

      {/* Create modal */}
      {showCreate && (
        <div className="fixed inset-0 bg-black/60 flex items-center justify-center z-50 p-4">
          <div className="bg-gray-900 border border-gray-800 rounded-2xl w-full max-w-sm p-6">
            <h2 className="text-white font-semibold mb-4">Create API Key</h2>
            <label className="text-sm text-gray-400">Key Name</label>
            <input
              value={newKeyName}
              onChange={e => setNewKeyName(e.target.value)}
              className="mt-1 w-full bg-gray-800 border border-gray-700 text-white rounded-lg px-3 py-2 focus:outline-none focus:border-violet-500"
              placeholder="Production key"
            />
            <div className="flex gap-3 mt-5">
              <button onClick={() => setShowCreate(false)} className="flex-1 bg-gray-800 text-gray-300 rounded-lg py-2 hover:bg-gray-700">Cancel</button>
              <button
                onClick={() => createMut.mutate({ name: newKeyName })}
                disabled={!newKeyName || createMut.isPending}
                className="flex-1 bg-violet-600 text-white rounded-lg py-2 hover:bg-violet-700 disabled:opacity-50"
              >
                {createMut.isPending ? 'Creating...' : 'Create'}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Keys list */}
      {keys.length === 0 ? (
        <div className="text-center py-16 bg-gray-900 border border-gray-800 rounded-xl">
          <Key size={36} className="text-gray-700 mx-auto mb-3" />
          <p className="text-gray-400">No API keys yet</p>
          <p className="text-gray-600 text-sm mt-1">Create a key to access ModelVault programmatically</p>
        </div>
      ) : (
        <div className="bg-gray-900 border border-gray-800 rounded-xl divide-y divide-gray-800">
          {keys.map((k: any) => (
            <div key={k.id} className="flex items-center justify-between p-4">
              <div className="flex items-center gap-3">
                <Key size={16} className="text-gray-500" />
                <div>
                  <p className="text-white text-sm font-medium">{k.name}</p>
                  <p className="text-gray-500 text-xs font-mono mt-0.5">{k.key_prefix}••••••••</p>
                </div>
              </div>
              <div className="flex items-center gap-4">
                <div className="text-right">
                  <p className={`text-xs ${k.is_active ? 'text-emerald-400' : 'text-gray-600'}`}>
                    {k.is_active ? 'Active' : 'Revoked'}
                  </p>
                  {k.last_used_at && (
                    <p className="text-xs text-gray-600">
                      Used {formatDistanceToNow(new Date(k.last_used_at), { addSuffix: true })}
                    </p>
                  )}
                </div>
                {k.is_active && (
                  <button
                    onClick={() => revokeMut.mutate(k.id)}
                    className="text-red-500 hover:text-red-400 p-1.5 hover:bg-red-900/20 rounded-lg transition"
                  >
                    <Trash2 size={15} />
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Usage example */}
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
        <h3 className="text-white font-medium mb-3 text-sm">Usage Example</h3>
        <pre className="bg-gray-950 text-emerald-400 text-xs rounded-lg p-4 overflow-x-auto font-mono">{`curl -X POST https://api.modelvault.ai/api/v1/inference/{model_id}/predict \\
  -H "X-API-Key: mv_your_key_here" \\
  -H "Content-Type: application/json" \\
  -d '{"inputs": {"text": "Hello world"}}'`}</pre>
      </div>
    </div>
  );
}
