import type { NextApiRequest, NextApiResponse } from 'next';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  const { mode } = req.query;
  const body = req.body;

  const backendUrl = process.env.BACKEND_URL || 'https://kairosinitiative-production.up.railway.app';
  const endpoint = mode === 'reflect'
    ? `${backendUrl}/kairos/reason`
    : `${backendUrl}/kairos`;

  try {
    const kairosRes = await fetch(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });

    const data = await kairosRes.json();
    res.status(kairosRes.status).json(data);
  } catch (err) {
    console.error('Kairos Proxy Error:', err);
    res.status(500).json({ error: 'Kairos Proxy Failed' });
  }
}
