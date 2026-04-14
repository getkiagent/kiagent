import { Workflow, Mail, ShoppingBag, Shield } from 'lucide-react'

const deliverables = [
  {
    icon: Workflow,
    title: 'n8n-Workflow auf deinem Stack',
    desc: 'Läuft in deiner eigenen n8n-Instanz oder bei uns. Du behältst volle Kontrolle über Code, Daten und Workflows — keine Lock-ins.',
  },
  {
    icon: Mail,
    title: 'Gmail-Draft-Automation',
    desc: 'Eingehende Support-Mails werden automatisch analysiert und als Entwurf in Gmail vorformuliert. Du prüfst und sendest — oder aktivierst Auto-Versand.',
  },
  {
    icon: ShoppingBag,
    title: 'Shop-Anbindung',
    desc: 'Direkt an Shopify, WooCommerce oder Shopware angebunden. Bestellstatus, Tracking und Retouren werden aus echten Daten beantwortet — nicht halluziniert.',
  },
  {
    icon: Shield,
    title: 'DSGVO-konform & EU-gehostet',
    desc: 'Alle Daten bleiben in der EU. Auftragsverarbeitungsvertrag inklusive. Keine US-Hyperscaler im Daten-Pfad deiner Kundenanfragen.',
  },
]

export default function Features() {
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
          <p className="eyebrow">Lieferumfang</p>
          <h2 className="display-l" style={{ marginBottom: '1rem' }}>
            Konkrete Deliverables.<br />
            <em style={{ color: 'var(--accent)', fontStyle: 'italic' }}>Keine Buzzwords.</em>
          </h2>
          <p className="lead">
            Was du nach zwei Wochen in der Hand hast — aufgeschlüsselt, nachvollziehbar, ohne Marketing-Nebel.
          </p>
        </div>

        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
          gap: '1.25rem',
        }}>
          {deliverables.map(({ icon: Icon, title, desc }) => (
            <article
              key={title}
              style={{
                background: 'var(--bg-elevated)',
                border: '1px solid var(--border)',
                borderRadius: 'var(--r-lg)',
                padding: '2rem',
                transition: 'border-color 0.25s ease, transform 0.25s ease, background 0.25s ease',
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
              <div style={{
                width: '44px',
                height: '44px',
                borderRadius: 'var(--r-sm)',
                background: 'var(--accent-soft)',
                border: '1px solid rgba(201, 166, 107, 0.25)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                marginBottom: '1.5rem',
              }}>
                <Icon size={20} color="#c9a66b" strokeWidth={1.75} />
              </div>
              <h3 style={{
                fontFamily: 'var(--font-serif)',
                fontSize: '1.25rem',
                fontWeight: 500,
                color: 'var(--text)',
                marginBottom: '0.625rem',
                letterSpacing: '-0.015em',
                lineHeight: 1.25,
              }}>
                {title}
              </h3>
              <p style={{
                color: 'var(--text-muted)',
                fontSize: '0.9375rem',
                lineHeight: 1.65,
              }}>
                {desc}
              </p>
            </article>
          ))}
        </div>
      </div>
    </section>
  )
}
