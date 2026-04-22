import { UserPlus, Clock, RefreshCcw } from 'lucide-react'

const pains = [
  {
    icon: UserPlus,
    stat: '€36.000 / Jahr',
    title: 'Eine Vollzeitkraft für Support',
    desc: 'Gehalt, Lohnnebenkosten, Einarbeitung — und trotzdem skaliert sie nicht in der Peak-Saison. Krankheitstage, Kündigung, Wiedereinstieg: der Kreislauf beginnt neu.',
  },
  {
    icon: Clock,
    stat: '9–17 Uhr',
    title: 'Support endet, wenn Kunden kaufen',
    desc: 'Bestellungen laufen abends und am Wochenende rein. Die Antwortzeit beträgt 4+ Stunden. Deine Konkurrenz antwortet in 2 Sekunden — rund um die Uhr.',
  },
  {
    icon: RefreshCcw,
    stat: '60–70 % aller Tickets',
    title: 'Immer die gleichen Fragen',
    desc: 'WISMO, Retouren, Lieferzeit, Produkt-FAQ. Jede Antwort ist Copy-Paste. Jede Stunde kostet dich Geld, die dein Team mit echter Kundenarbeit verbringen könnte.',
  },
]

export default function Pain() {
  return (
    <section
      id="problem"
      className="section"
      style={{
        background: 'var(--bg-elevated)',
        borderTop: '1px solid var(--border)',
      }}
    >
      <div className="container">
        <div style={{ marginBottom: '3.5rem', maxWidth: '680px' }}>
          <p className="eyebrow">Das Problem</p>
          <h2 className="display-l" style={{ marginBottom: '1rem' }}>
            Support-Personal ist teuer,<br />
            <em style={{ color: 'var(--accent)', fontStyle: 'italic' }}>starr und nicht skalierbar.</em>
          </h2>
          <p className="lead">
            Die meisten Shops wissen das — und stellen trotzdem ein. Weil es keine Alternative gab. Bis jetzt.
          </p>
        </div>

        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
          gap: '1.25rem',
        }}>
          {pains.map(({ icon: Icon, stat, title, desc }) => (
            <article
              key={title}
              style={{
                background: 'var(--bg)',
                border: '1px solid var(--border)',
                borderRadius: 'var(--r-lg)',
                padding: '2rem',
              }}
            >
              <div style={{
                width: '44px',
                height: '44px',
                borderRadius: 'var(--r-sm)',
                background: 'rgba(201, 166, 107, 0.06)',
                border: '1px solid rgba(201, 166, 107, 0.15)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                marginBottom: '1.25rem',
              }}>
                <Icon size={20} color="var(--accent)" strokeWidth={1.75} style={{ opacity: 0.7 }} />
              </div>
              <div style={{
                fontFamily: 'var(--font-serif)',
                fontSize: 'clamp(1.35rem, 2.5vw, 1.75rem)',
                fontWeight: 500,
                color: 'var(--accent)',
                letterSpacing: '-0.02em',
                lineHeight: 1,
                marginBottom: '0.5rem',
              }}>
                {stat}
              </div>
              <h3 style={{
                fontFamily: 'var(--font-serif)',
                fontSize: '1.1rem',
                fontWeight: 500,
                color: 'var(--text)',
                marginBottom: '0.625rem',
                letterSpacing: '-0.01em',
                lineHeight: 1.3,
              }}>
                {title}
              </h3>
              <p style={{
                color: 'var(--text-muted)',
                fontSize: '0.9rem',
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
