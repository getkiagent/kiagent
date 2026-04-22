import { useState, useEffect, useRef } from 'react'

const SCENARIOS = [
  {
    tag: 'WISMO',
    user: 'Wo ist meine Bestellung #GW-4821? Ich warte schon 4 Tage.',
    bot: 'Hallo! Deine Bestellung #GW-4821 wurde heute von DHL abgeholt.\n\n📦 Status: In Zustellung\n🕙 Lieferung: Morgen, 10–14 Uhr\n\n→ Tracking: dhl.de/track/GW4821',
    time: '1.4 Sek',
  },
  {
    tag: 'Retoure',
    user: 'Ich möchte das Serum zurückschicken — falsche Farbe.',
    bot: 'Kein Problem! Retourenantrag erstellt:\n\n🏷 Retourennr.: RT-2024-0834\n📧 Label → max.muster@web.de\n\nRückerstattung in 3–5 Werktagen nach Eingang.',
    time: '1.8 Sek',
  },
  {
    tag: 'Produktfrage',
    user: 'Ist das Vitamin-C-Serum auch für empfindliche Haut?',
    bot: 'Ja! Das Serum ist dermatologisch getestet — auch für empfindliche Haut.\n\n✓ Ohne Parfüm & Parabene\n✓ pH-neutral formuliert\n✓ 95 % positiver Bewertungen nach 4 Wochen',
    time: '1.2 Sek',
  },
]

export default function ChatDemo() {
  const [idx, setIdx] = useState(0)
  const [phase, setPhase] = useState('user')
  const t = useRef()

  useEffect(() => {
    clearTimeout(t.current)
    if (phase === 'user') {
      t.current = setTimeout(() => setPhase('typing'), 900)
    } else if (phase === 'typing') {
      t.current = setTimeout(() => setPhase('bot'), 1500)
    } else if (phase === 'bot') {
      t.current = setTimeout(() => {
        setPhase('user')
        setIdx(i => (i + 1) % SCENARIOS.length)
      }, 4200)
    }
    return () => clearTimeout(t.current)
  }, [phase, idx])

  const s = SCENARIOS[idx]

  return (
    <div style={{
      background: '#0d1018',
      border: '1px solid var(--border-strong)',
      borderRadius: 'var(--r-lg)',
      overflow: 'hidden',
      fontFamily: 'var(--font-sans)',
      boxShadow: '0 24px 60px -12px rgba(0,0,0,0.6), 0 0 0 1px rgba(201,166,107,0.06)',
      flex: '1 1 380px',
      minWidth: 0,
    }}>
      <style>{`
        @keyframes fadeSlideUp {
          from { opacity: 0; transform: translateY(8px); }
          to   { opacity: 1; transform: translateY(0); }
        }
        @keyframes dotBounce {
          0%, 60%, 100% { transform: translateY(0); opacity: 0.4; }
          30% { transform: translateY(-5px); opacity: 1; }
        }
      `}</style>

      {/* Header */}
      <div style={{
        padding: '0.875rem 1.125rem',
        borderBottom: '1px solid var(--border)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        background: '#0b0e14',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
          <div style={{
            width: '30px', height: '30px', borderRadius: '50%',
            background: 'var(--accent-soft)',
            border: '1px solid rgba(201,166,107,0.25)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            fontSize: '0.85rem',
          }}>✨</div>
          <div>
            <div style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--text)', lineHeight: 1.2 }}>
              GlowLab Support
            </div>
            <div style={{ fontSize: '0.65rem', color: '#22c55e', display: 'flex', alignItems: 'center', gap: '0.3rem' }}>
              <span style={{ width: 5, height: 5, borderRadius: '50%', background: '#22c55e', display: 'inline-block' }} />
              KI-Agent aktiv
            </div>
          </div>
        </div>
        <div style={{
          fontSize: '0.62rem', fontWeight: 600, letterSpacing: '0.06em',
          padding: '0.2rem 0.6rem', borderRadius: '2rem',
          background: 'var(--accent-soft)', color: 'var(--accent)',
          textTransform: 'uppercase',
        }}>
          {s.tag}
        </div>
      </div>

      {/* Messages */}
      <div style={{
        padding: '1.25rem 1rem',
        minHeight: '230px',
        display: 'flex', flexDirection: 'column', gap: '0.875rem',
      }}>
        {/* User bubble */}
        {(phase === 'user' || phase === 'typing' || phase === 'bot') && (
          <div key={`u-${idx}`} style={{ display: 'flex', justifyContent: 'flex-end' }}>
            <div style={{
              background: '#1d2438',
              border: '1px solid var(--border)',
              borderRadius: '1rem 1rem 0.2rem 1rem',
              padding: '0.7rem 0.9rem',
              maxWidth: '82%',
              fontSize: '0.8rem',
              color: 'var(--text)',
              lineHeight: 1.55,
              animation: 'fadeSlideUp 0.3s ease',
            }}>
              {s.user}
            </div>
          </div>
        )}

        {/* Typing indicator */}
        {phase === 'typing' && (
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <div style={{
              width: '26px', height: '26px', borderRadius: '50%',
              background: 'var(--accent-soft)', display: 'flex',
              alignItems: 'center', justifyContent: 'center',
              fontSize: '0.7rem', flexShrink: 0,
            }}>🤖</div>
            <div style={{
              background: 'var(--bg-elevated)',
              border: '1px solid var(--border)',
              borderRadius: '1rem 1rem 1rem 0.2rem',
              padding: '0.7rem 0.9rem',
              display: 'flex', gap: '0.3rem', alignItems: 'center',
            }}>
              {[0, 1, 2].map(i => (
                <span key={i} style={{
                  width: 5, height: 5, borderRadius: '50%',
                  background: 'var(--text-subtle)', display: 'inline-block',
                  animation: `dotBounce 1.1s ease ${i * 0.14}s infinite`,
                }} />
              ))}
            </div>
          </div>
        )}

        {/* Bot reply */}
        {phase === 'bot' && (
          <div key={`b-${idx}`} style={{ display: 'flex', alignItems: 'flex-start', gap: '0.5rem' }}>
            <div style={{
              width: '26px', height: '26px', borderRadius: '50%',
              background: 'var(--accent-soft)', display: 'flex',
              alignItems: 'center', justifyContent: 'center',
              fontSize: '0.7rem', flexShrink: 0, marginTop: '2px',
            }}>🤖</div>
            <div>
              <div style={{
                background: 'var(--bg-elevated)',
                border: '1px solid var(--border)',
                borderRadius: '1rem 1rem 1rem 0.2rem',
                padding: '0.7rem 0.9rem',
                maxWidth: '88%',
                fontSize: '0.8rem',
                color: 'var(--text)',
                lineHeight: 1.65,
                animation: 'fadeSlideUp 0.3s ease',
                whiteSpace: 'pre-line',
              }}>
                {s.bot}
              </div>
              <div style={{
                marginTop: '0.3rem', fontSize: '0.65rem',
                color: 'var(--accent)',
                display: 'flex', alignItems: 'center', gap: '0.25rem',
                paddingLeft: '0.2rem',
              }}>
                ⚡ Antwort in {s.time}
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Scenario tabs */}
      <div style={{
        padding: '0.75rem 1rem',
        borderTop: '1px solid var(--border)',
        background: '#0b0e14',
        display: 'flex', gap: '0.4rem', flexWrap: 'wrap',
      }}>
        {SCENARIOS.map((sc, i) => (
          <button
            key={sc.tag}
            onClick={() => { setIdx(i); setPhase('user') }}
            style={{
              padding: '0.28rem 0.7rem',
              borderRadius: '2rem',
              border: '1px solid',
              borderColor: i === idx ? 'var(--accent)' : 'var(--border)',
              background: i === idx ? 'var(--accent-soft)' : 'transparent',
              color: i === idx ? 'var(--accent)' : 'var(--text-subtle)',
              fontSize: '0.68rem', fontWeight: 500,
              cursor: 'pointer',
              transition: 'all 0.2s ease',
            }}
          >
            {sc.tag}
          </button>
        ))}
      </div>
    </div>
  )
}
