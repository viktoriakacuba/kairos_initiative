export default async function handler(req, res) {
    const { method, query } = req;
  
    if (method !== 'POST') {
      return res.status(405).json({ error: 'Method Not Allowed' });
    }
  
    const { message, input } = req.body;
    const user_id = 'public-user';
    const mode = query.mode || 'fast';
  
    const payload = mode === 'fast' ? { message, user_id } : { input, user_id };
  
    const targetUrl =
      mode === 'fast'
        ? 'https://kairosinitiative-production.up.railway.app/kairos'
        : 'https://kairosinitiative-production.up.railway.app/kairos/reason';
  
    try {
      const response = await fetch(targetUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
  
      const data = await response.json();
      return res.status(200).json(data);
    } catch (err) {
      console.error('Proxy error:', err);
      return res.status(500).json({ error: 'Internal proxy error' });
    }
  }
  