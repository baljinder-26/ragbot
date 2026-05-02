const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export async function sendChat(message, userId) {
  const res = await fetch(`${BASE_URL}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, user_id: userId }),
  });
  if (!res.ok) throw new Error('Chat request failed');
  return res.json();
}

export async function uploadPDF(file, userId) {
  const form = new FormData();
  form.append('file', file);
  form.append('user_id', userId);
  const res = await fetch(`${BASE_URL}/upload-pdf`, {
    method: 'POST',
    body: form,
  });
  if (!res.ok) throw new Error('Upload failed');
  return res.json();
}

export async function listPDFs(userId) {
  const res = await fetch(`${BASE_URL}/list-pdfs?user_id=${userId}`);
  if (!res.ok) throw new Error('List failed');
  return res.json();
}

export async function deletePDF(filename, userId) {
  const res = await fetch(`${BASE_URL}/delete-pdf`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ filename, user_id: userId }),
  });
  if (!res.ok) throw new Error('Delete failed');
  return res.json();
}

export async function clearDatabase(userId) {
  const form = new FormData();
  form.append('user_id', userId);
  const res = await fetch(`${BASE_URL}/clear-database`, {
    method: 'POST',
    body: form,
  });
  if (!res.ok) throw new Error('Clear failed');
  return res.json();
}
