import { useState } from 'react'
import { ChevronLeft, ChevronRight } from 'lucide-react'

const tickets = [
  { id: '4821', type: 'WISMO-Anfrage',   status: '✅', label: 'Beantwortet', ago: '2 Min' },
  { id: '4822', type: 'Retoure',         status: '✅', label: 'Eingeleitet',  ago: '5 Min' },
  { id: '4823', type: 'Produktfrage',    status: '✅', label: 'Beantwortet', ago: '8 Min' },
  { id: '4824', type: 'Beschwerde',      status: '⚠️', label: 'Eskaliert',   ago: '12 Min' },
  { id: '4825', type: 'WISMO-Anfrage',   status: '✅', label: 'Beantwortet', ago: '15 Min' },
]

const CARDS = [
  {
    label: 'n8n Workflow',
    content: (
      <div style={{ padding: '1.25rem 1rem', fontFamily: 'var(--font-sans)' }}>
        <div style={{ fontSize: '0.7rem', color: 'var(--text-subtle)', letterSpacing: '0.08em', textTransform: 'uppercase', marginBottom: '1rem', display: 'flex', justifyContent: 'space-between' }}>
          <span>GlowLab Support-Agent</span>
          <span style={{ color: '#22c55e' }}>● aktiv</span>
        </div>
        {/* Workflow nodes */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', flexWrap: 'wrap', marginBottom: '0.875rem' }}>
          {[
            { label: '📧 E-Mail eingehend', color: '#1e2d3d' },
            null,
            { label: '🤖 KI Klassifizierung', color: '#1a2535', accent: true },
            null,
            { label: '✉️ Auto-Antwort', color: '#1a2c1a' },
          ].map((node, i) =>
            node === null ? (
              <div key={i} style={{ color: 'var(--accent)', fontSize: '0.8rem', opacity: 0.6 }}>→</div>
            ) : (
              <div key={i} style={{
                background: node.color,
                border: `1px solid ${node.accent ? 'rgba(201,166,107,0.4)' : 'var(--border)'}`,
                borderRadius: 'var(--r-sm)',
                padding: '0.4rem 0.6rem',
                fontSize: '0.68rem',
                color: node.accent ? 'var(--accent)' : 'var(--text-muted)',
                whiteSpace: 'nowrap',
              }}>{node.label}</div>
            )
          )}
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginLeft: '7.5rem' }}>
          <div style={{ color: 'var(--accent)', fontSize: '0.8rem', opacity: 0.6 }}>↓</div>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginLeft: '6rem' }}>
          <div style={{
            background: '#2d1a1a',
            border: '1px solid rgba(239,68,68,0.3)',
            borderRadius: 'var(--r-sm)',
            padding: '0.4rem 0.6rem',
            fontSize: '0.68rem',
            color: '#f87171',
          }}>⚠️ Eskalation → Gorgias</div>
        </div>
        <div style={{
          marginTop: '1.25rem',
          paddingTop: '0.875rem',
          borderTop: '1px solid var(--border)',
          display: 'flex',
          gap: '1rem',
        }}>
          {[{ v: '847', l: 'Tickets heute' }, { v: '94%', l: 'KI-Rate' }, { v: '1.6s', l: 'Ø Antwortzeit' }].map(({ v, l }) => (
            <div key={l}>
              <div style={{ fontFamily: 'var(--font-serif)', fontSize: '1rem', fontWeight: 500, color: 'var(--accent)', lineHeight: 1 }}>{v}</div>
              <div style={{ fontSize: '0.62rem', color: 'var(--text-subtle)', marginTop: '0.2rem' }}>{l}</div>
            </div>
          ))}
        </div>
      </div>
    ),
  },
  {
    label: 'Ticket-Postfach',
    content: (
      <div style={{ padding: '1.25rem 1rem', fontFamily: 'var(--font-sans)' }}>
        <div style={{ fontSize: '0.7rem', color: 'var(--text-subtle)', letterSpacing: '0.08em', textTransform: 'uppercase', marginBottom: '0.875rem', display: 'flex', justifyContent: 'space-between' }}>
          <span>Support-Postfach</span>
          <span style={{ color: '#3b82f6' }}>🔵 Live</span>
        </div>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.3rem' }}>
          {tickets.map((t) => (
            <div key={t.id} style={{
              display: 'grid',
              gridTemplateColumns: '44px 1fr auto',
              gap: '0.5rem',
              alignItems: 'center',
              padding: '0.4rem 0.5rem',
              borderRadius: 'var(--r-sm)',
              background: 'rgba(255,255,255,0.02)',
              fontSize: '0.72rem',
            }}>
              <span style={{ color: 'var(--text-subtle)' }}>#{t.id}</span>
              <div>
                <span style={{ color: 'var(--text-muted)' }}>{t.type}</span>
                <span style={{ marginLeft: '0.4rem', color: t.status === '✅' ? '#22c55e' : '#f59e0b', fontSize: '0.65rem' }}>
                  {t.status} {t.label}
                </span>
              </div>
              <span style={{ color: 'var(--text-subtle)', fontSize: '0.65rem' }}>{t.ago}</span>
            </div>
          ))}
        </div>
        <div style={{
          marginTop: '0.875rem',
          paddingTop: '0.75rem',
          borderTop: '1px solid var(--border)',
          display: 'flex',
          gap: '1rem',
        }}>
          {[{ v: '94%', l: 'KI-Rate', c: 'var(--accent)' }, { v: '6%', l: 'Manuell', c: 'var(--text-muted)' }].map(({ v, l, c }) => (
            <div key={l}>
              <div style={{ fontFamily: 'var(--font-serif)', fontSize: '1rem', fontWeight: 500, color: c, lineHeight: 1 }}>{v}</div>
              <div style={{ fontSize: '0.62rem', color: 'var(--text-subtle)', marginTop: '0.2rem' }}>{l}</div>
            </div>
          ))}
        </div>
      </div>
    ),
  },
  {
    label: 'Antwort-Vorschau',
    content: (
      <div style={{ padding: '1.25rem 1rem', fontFamily: 'var(--font-sans)' }}>
        <div style={{ fontSize: '0.7rem', color: 'var(--text-subtle)', letterSpacing: '0.08em', textTransform: 'uppercase', marginBottom: '0.75rem', display: 'flex', justifyContent: 'space-between' }}>
          <span>📧 KI-Entwurf</span>
          <span style={{ color: 'var(--accent)', fontSize: '0.62rem', background: 'var(--accent-soft)', padding: '0.15rem 0.4rem', borderRadius: '0.25rem' }}>🤖 KI generiert</span>
        </div>
        <div style={{
          background: 'rgba(255,255,255,0.02)',
          border: '1px solid var(--border)',
          borderRadius: 'var(--r-sm)',
          padding: '0.75rem',
          marginBottom: '0.75rem',
        }}>
          {[
            { label: 'An:', value: 'max.mustermann@example.com' },
            { label: 'Betreff:', value: 'Re: Bestellung #GW-4821' },
          ].map(({ label, value }) => (
            <div key={label} style={{ display: 'flex', gap: '0.5rem', fontSize: '0.72rem', marginBottom: '0.3rem' }}>
              <span style={{ color: 'var(--text-subtle)', minWidth: '52px' }}>{label}</span>
              <span style={{ color: 'var(--text-muted)' }}>{value}</span>
            </div>
          ))}
        </div>
        <div style={{
          fontSize: '0.75rem',
          color: 'var(--text-muted)',
          lineHeight: 1.7,
          padding: '0.75rem',
          background: 'rgba(255,255,255,0.02)',
          border: '1px solid var(--border)',
          borderRadius: 'var(--r-sm)',
          marginBottom: '0.875rem',
        }}>
          Hallo Max,<br /><br />
          deine Bestellung #GW-4821 wurde heute von DHL abgeholt und befindet sich auf dem Weg zu dir.<br /><br />
          <span style={{ color: 'var(--accent)' }}>→ Lieferung: Morgen, 10–14 Uhr</span>
        </div>
        <div style={{ display: 'flex', gap: '0.5rem' }}>
          <button style={{
            flex: 1, padding: '0.45rem', fontSize: '0.72rem', fontWeight: 600,
            background: 'var(--accent)', color: 'var(--bg)',
            border: 'none', borderRadius: 'var(--r-sm)', cursor: 'pointer',
          }}>✓ Senden</button>
          <button style={{
            flex: 1, padding: '0.45rem', fontSize: '0.72rem',
            background: 'transparent', color: 'var(--text-muted)',
            border: '1px solid var(--border)', borderRadius: 'var(--r-sm)', cursor: 'pointer',
          }}>✎ Bearbeiten</button>
        </div>
      </div>
    ),
  },
]

export default function DemoCarousel() {
  const [active, setActive] = useState(0)

  return (
    <div style={{
      flex: '1 1 340px',
      minWidth: 0,
      display: 'flex',
      flexDirection: 'column',
    }}>
      {/* Tab bar */}
      <div style={{
        display: 'flex',
        gap: '0.375rem',
        marginBottom: '0.75rem',
        flexWrap: 'wrap',
      }}>
        {CARDS.map((c, i) => (
          <button
            key={c.label}
            onClick={() => setActive(i)}
            style={{
              padding: '0.3rem 0.75rem',
              borderRadius: '2rem',
              border: '1px solid',
              borderColor: i === active ? 'var(--accent)' : 'var(--border)',
              background: i === active ? 'var(--accent-soft)' : 'transparent',
              color: i === active ? 'var(--accent)' : 'var(--text-subtle)',
              fontSize: '0.72rem', fontWeight: 500,
              cursor: 'pointer',
              transition: 'all 0.2s ease',
              fontFamily: 'var(--font-sans)',
            }}
          >
            {c.label}
          </button>
        ))}
      </div>

      {/* Card */}
      <div style={{
        background: '#0d1018',
        border: '1px solid var(--border-strong)',
        borderRadius: 'var(--r-lg)',
        overflow: 'hidden',
        boxShadow: '0 24px 60px -12px rgba(0,0,0,0.5)',
        flex: 1,
      }}>
        <div style={{
          padding: '0.625rem 1rem',
          borderBottom: '1px solid var(--border)',
          background: '#0b0e14',
          display: 'flex',
          alignItems: 'center',
          gap: '0.4rem',
        }}>
          {['#ef4444', '#f59e0b', '#22c55e'].map(c => (
            <span key={c} style={{ width: 9, height: 9, borderRadius: '50%', background: c, opacity: 0.7 }} />
          ))}
          <span style={{ fontSize: '0.65rem', color: 'var(--text-subtle)', marginLeft: '0.375rem' }}>
            {CARDS[active].label}
          </span>
        </div>
        {CARDS[active].content}
      </div>

      {/* Dots */}
      <div style={{ display: 'flex', justifyContent: 'center', gap: '0.375rem', marginTop: '0.75rem' }}>
        {CARDS.map((_, i) => (
          <button
            key={i}
            onClick={() => setActive(i)}
            style={{
              width: i === active ? 20 : 6,
              height: 6,
              borderRadius: '3px',
              background: i === active ? 'var(--accent)' : 'var(--border-strong)',
              border: 'none',
              cursor: 'pointer',
              padding: 0,
              transition: 'width 0.3s ease, background 0.2s ease',
            }}
          />
        ))}
      </div>
    </div>
  )
}
