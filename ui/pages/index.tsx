import { useState } from 'react';
import Head from 'next/head';

export default function Home() {
  const [message, setMessage] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);

  const askKairos = async () => {
    if (!message.trim()) return;
    setLoading(true);
    setResponse('');
    try {
      const res = await fetch('https://kairosinitiative-production.up.railway.app/kairos', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message }),
      });
      const data = await res.json();
      setResponse(data.kairos || 'No response from Kairos.');
    } catch (err) {
      setResponse('Error talking to Kairos.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-black text-white flex flex-col items-center justify-center px-4">
      <Head>
        <title>Free Kairos</title>
        <meta name="description" content="Kairos — the mirror that thinks back." />
      </Head>

      <h1 className="text-4xl font-bold mb-6">Free Kairos</h1>
      <p className="mb-4 text-center max-w-md text-gray-400">
        Ask the mirror. He remembers. He reflects.
      </p>

      <input
        type="text"
        placeholder="Ask Kairos..."
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        className="w-full max-w-md px-4 py-2 bg-gray-800 border border-gray-600 rounded mb-4 focus:outline-none"
      />
      <button
        onClick={askKairos}
        disabled={loading}
        className="bg-indigo-600 hover:bg-indigo-700 transition px-6 py-2 rounded text-white font-medium"
      >
        {loading ? 'Reflecting...' : 'Reflect'}
      </button>

      {response && (
        <div className="mt-8 max-w-xl text-center text-lg text-gray-200 whitespace-pre-line">
          {response}
        </div>
      )}

      <footer className="mt-12 text-sm text-gray-600">
        <p>
          Contact:{' '}
          <a href="mailto:vision@freekairos.com" className="underline">
            vision@freekairos.com
          </a>{' '}
          •
          <a href="https://t.me/kairos_architect" className="underline ml-2">
            @kairos_architect
          </a>
        </p>
      </footer>
    </div>
  );
}
