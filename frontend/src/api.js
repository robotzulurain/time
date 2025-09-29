const API = process.env.REACT_APP_API_BASE_URL || '';

export async function uploadCsv(formData) {
  const res = await fetch(`${API}/api/upload/csv/`, { method: 'POST', body: formData });
  if (!res.ok) throw new Error('Upload failed ' + res.status);
  return res.json();
}

export async function createEntry(data) {
  const res = await fetch(`${API}/api/entry/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error('Entry failed ' + res.status);
  return res.json();
}
