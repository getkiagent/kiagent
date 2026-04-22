import { MessageSquare, Star, ShoppingBag, Target } from 'lucide-react'

const products = [
  {
    icon: MessageSquare,
    title: 'KI-Support-Agent',
    tag: 'Kernprodukt',
    desc: '60–70 % aller Tickets vollautomatisch beantwortet — WISMO, Retouren, Produktfragen. Direkt an deinen Shop angebunden, live ab Tag 14.',
    benefits: [
      'Spart 1–2 FTE Personalkosten',
      '24/7 ohne Schichtbetrieb',
      'Antworten aus echten Shopify-Daten — keine Halluzinationen',
    ],
  },
  {
    icon: Star,
    title: 'Review & UGC-Automation',
    tag: 'Add-on',
    desc: 'KI antwortet automatisch auf Google- und Trustpilot-Bewertungen im richtigen Ton. Post-Purchase-Flows fordern aktiv Fotos und UGC an.',
    benefits: [
      'Bessere Review-Scores ohne manuellen Aufwand',
      'Mehr authentischer Content für Produktseiten',
      'Beauty-Brands: durchschnittlich +18 % Conversion durch UGC',
    ],
  },
  {
    icon: ShoppingBag,
    title: 'Pre-Sales Chatbot',
    tag: 'Add-on',
    desc: 'KI-Berater auf deiner Website, der Kunden zum passenden Produkt führt. Senkt Retouren durch bessere Kaufentscheidungen — 24/7 verfügbar.',
    benefits: [
      'Höhere Add-to-Cart-Rate',
      'Weniger Rückfragen vor dem Kauf',
      'Weniger Retouren durch schlechte Produktmatches',
    ],
  },
  {
    icon: Target,
    title: 'Lead Generator & Outreach',
    tag: 'Add-on',
    desc: 'Automatisierte Identifikation von Zielkunden anhand von Hiring-Signalen und Shop-Profilen — inklusive KI-personalisierter Outreach-E-Mails.',
    benefits: [
      'Skalierbare Neukundengewinnung ohne Sales-Team',
      'Reply-Raten von 15–25 % statt klassischer Kaltakquise',
      'Läuft vollständig in deinem Stack',
    ],
  },
]

export default function Products() {
  return (
    <section
      id="leistungen"
      className="section"
      style={{
        background: 'var(--bg)',
        borderTop: '1px solid var(--border)',
      }}
    >
      <div className="container">
        <div style={{ marginBottom: '3.5rem', maxWidth: '680px' }}>
          <p className="eyebrow">Leistungen</p>
          <h2 className="display-l" style={{ marginBottom: '1rem' }}>
            Vier Produkte.<br />
            <em style={{ color: 'var(--accent)', fontStyle: 'italic' }}>Ein Ziel: weniger Aufwand.</em>
          </h2>
          <p className="lead">
            Einzeln buchbar oder kombiniert. Alles auf deinem Stack, alles DSGVO-konform, alles mit direktem ROI.
          </p>
        </div>

        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(420px, 1fr))',
          gap: '1.25rem',
        }}>
          {products.map(({ icon: Icon, title, tag, desc, benefits }) => (
            <article
              key={title}
              style={{
                background: 'var(--bg-elevated)',
                border: '1px solid var(--border)',
                borderRadius: 'var(--r-lg)',
                padding: '2rem',
                transition: 'border-color 0.25s ease, transform 0.25s ease',
                display: 'flex',
                flexDirection: 'column',
                gap: '1.25rem',
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.borderColor = 'var(--accent)'
                e.currentTarget.style.transform = 'translateY(-2px)'
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.borderColor = 'var(--border)'
                e.currentTarget.style.transform = 'translateY(0)'
              }}
            >
              <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', gap: '1rem' }}>
                <div style={{
                  width: '48px', height: '48px',
                  borderRadius: 'var(--r-sm)',
                  background: 'var(--accent-soft)',
                  border: '1px solid rgba(201, 166, 107, 0.25)',
                  display: 'flex', alignItems: 'center', justifyContent: 'center',
                  flexShrink: 0,
                }}>
                  <Icon size={22} color="var(--accent)" strokeWidth={1.6} />
                </div>
                <span style={{
                  fontSize: '0.65rem', fontWeight: 600,
                  letterSpacing: '0.07em', textTransform: 'uppercase',
                  padding: '0.25rem 0.625rem', borderRadius: '2rem',
                  background: tag === 'Kernprodukt' ? 'var(--accent-soft)' : 'rgba(255,255,255,0.04)',
                  border: `1px solid ${tag === 'Kernprodukt' ? 'rgba(201,166,107,0.3)' : 'var(--border)'}`,
                  color: tag === 'Kernprodukt' ? 'var(--accent)' : 'var(--text-subtle)',
                }}>
                  {tag}
                </span>
              </div>

              <div>
                <h3 style={{
                  fontFamily: 'var(--font-serif)',
                  fontSize: '1.3rem', fontWeight: 500,
                  color: 'var(--text)', letterSpacing: '-0.015em',
                  lineHeight: 1.25, marginBottom: '0.625rem',
                }}>
                  {title}
                </h3>
                <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', lineHeight: 1.65 }}>
                  {desc}
                </p>
              </div>

              <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '0.45rem' }}>
                {benefits.map((b) => (
                  <li key={b} style={{
                    display: 'flex', alignItems: 'flex-start', gap: '0.5rem',
                    fontSize: '0.85rem', color: 'var(--text-subtle)',
                  }}>
                    <span style={{
                      width: 5, height: 5, borderRadius: '50%',
                      background: 'var(--accent)', opacity: 0.7,
                      flexShrink: 0, marginTop: '0.45rem',
                    }} />
                    {b}
                  </li>
                ))}
              </ul>
            </article>
          ))}
        </div>
      </div>
    </section>
  )
}
