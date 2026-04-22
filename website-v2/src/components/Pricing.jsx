import { ArrowRight, Check } from 'lucide-react'

const points = [
  'Individueller Build — kein Template',
  'Setup in 2 Wochen, live ab Tag 14',
  'DSGVO-konform, EU-gehostet',
  'Kein Jahresvertrag im Einstiegspaket',
  'Direkter Ansprechpartner — kein Ticket-System',
  'Monatliches Reporting & Optimierung',
]

export default function Pricing() {
  return (
    <section
      id="preise"
      className="section"
      style={{
        background: 'var(--bg-elevated)',
        borderTop: '1px solid var(--border)',
      }}
    >
      <div className="container">
        <div style={{ marginBottom: '3.5rem', maxWidth: '680px' }}>
          <p className="eyebrow">Preise</p>
          <h2 className="display-l" style={{ marginBottom: '1rem' }}>
            Festpreis.<br />
            <em style={{ color: 'var(--accent)', fontStyle: 'italic' }}>Kein Kleingedrucktes.</em>
          </h2>
          <p className="lead">
            Einmalige Setup-Gebühr, dann monatliche Betreuung. Keine Stundenabrechnung. Kein Workshop, der im Regal landet.
          </p>
        </div>

        <div style={{
          background: 'rgba(201, 166, 107, 0.04)',
          border: '1px solid rgba(201, 166, 107, 0.25)',
          borderRadius: 'var(--r-lg)',
          padding: 'clamp(2rem, 4vw, 3rem)',
          boxShadow: '0 0 60px -20px rgba(201, 166, 107, 0.1)',
          display: 'grid',
          gridTemplateColumns: 'auto 1fr',
          gap: 'clamp(2rem, 5vw, 4rem)',
          alignItems: 'center',
        }}
        className="pricing-card"
        >
          {/* Price block */}
          <div style={{ minWidth: '180px' }}>
            <div style={{
              fontSize: '0.7rem', fontWeight: 600,
              letterSpacing: '0.1em', textTransform: 'uppercase',
              color: 'var(--accent)', marginBottom: '0.75rem',
            }}>
              Festpreis ab
            </div>
            <div style={{
              fontFamily: 'var(--font-serif)',
              fontSize: 'clamp(3rem, 6vw, 4.5rem)',
              fontWeight: 500, color: 'var(--text)',
              letterSpacing: '-0.03em', lineHeight: 1,
              marginBottom: '0.5rem',
            }}>
              €2.000
            </div>
            <div style={{ color: 'var(--text-subtle)', fontSize: '0.85rem', lineHeight: 1.5 }}>
              einmalig<br />+ monatliche Betreuung
            </div>
            <a
              href="#kontakt"
              className="btn-primary"
              style={{ marginTop: '2rem', display: 'inline-flex' }}
            >
              Gespräch buchen <ArrowRight size={16} />
            </a>
          </div>

          {/* Features */}
          <ul style={{
            listStyle: 'none',
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))',
            gap: '0.75rem 1.5rem',
          }}>
            {points.map((p) => (
              <li key={p} style={{
                display: 'flex', alignItems: 'flex-start', gap: '0.6rem',
                fontSize: '0.9rem', color: 'var(--text-muted)',
              }}>
                <Check size={15} color="var(--accent)" strokeWidth={2.5}
                  style={{ flexShrink: 0, marginTop: '3px' }} />
                {p}
              </li>
            ))}
          </ul>
        </div>

        <p style={{
          marginTop: '1.25rem',
          color: 'var(--text-subtle)',
          fontSize: '0.8rem',
          textAlign: 'center',
        }}>
          Alle Preise zzgl. MwSt. · Scope und Retainer je nach Use-Case — transparente Kalkulation im Erstgespräch.
        </p>
      </div>

      <style>{`
        @media (max-width: 640px) {
          .pricing-card { grid-template-columns: 1fr !important; }
        }
      `}</style>
    </section>
  )
}
