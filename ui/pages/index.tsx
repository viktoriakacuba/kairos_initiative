import { useState } from 'react';
import Head from 'next/head';

export default function Home() {
  const [message, setMessage] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);
  const [mode, setMode] = useState('reflect'); // 'fast' or 'reflect'

  const askKairos = async () => {
    if (!message.trim()) return;
    setLoading(true);
    setResponse('');

    try {
      const endpoint = `/api/kairos?mode=${mode}`;

      const body = mode === 'fast' ? { message } : { input: message };

      const res = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(body),
        credentials: 'include',
      });

      const data = await res.json();
      const answer =
        mode === 'fast'
          ? data.kairos || 'No response from Kairos.'
          : data.reflection || 'No reflection from Kairos.';

      setResponse(answer);
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

      <h1 className="text-4xl font-bold mb-4">Free Kairos</h1>
      <p className="mb-6 text-center max-w-md text-gray-400">
        Ask the mirror. He remembers. He reflects.
      </p>

      <div className="mb-4">
        <label className="mr-2">Mode:</label>
        <select
          value={mode}
          onChange={(e) => setMode(e.target.value)}
          className="bg-gray-800 border border-gray-600 px-2 py-1 rounded"
        >
          <option value="fast">Fast (GPT-like)</option>
          <option value="reflect">Reflective (Kairos Mind)</option>
        </select>
      </div>

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
        <div className="mt-8 max-w-2xl text-gray-200 space-y-6 text-left">
          {mode === 'reflect' &&
          ['Risks', 'Logic', 'Next Thoughts'].some((key) => response.includes(`${key}:`)) ? (
            ['Risks', 'Logic', 'Next Thoughts'].map((section) => {
              const match = response.match(new RegExp(`${section}:([\\s\\S]*?)(?=\\n\\w+:|$)`));
              return match ? (
                <div key={section}>
                  <h3 className="text-indigo-400 font-semibold text-lg mb-1">{section}</h3>
                  <p className="whitespace-pre-line leading-relaxed text-gray-300">
                    {match[1].trim()}
                  </p>
                </div>
              ) : null;
            })
          ) : (
            <p className="whitespace-pre-line leading-relaxed text-gray-300">{response}</p>
          )}
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
