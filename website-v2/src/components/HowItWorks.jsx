const steps = [
  {
    num: '01',
    title: 'Analyse',
    time: '30 Minuten',
    desc: 'Wir schauen deinen Support-Alltag, deine häufigsten Ticket-Typen und deinen Stack an. Du bekommst eine ehrliche Einschätzung — auch wenn KI bei dir (noch) nicht sinnvoll ist.',
  },
  {
    num: '02',
    title: 'Bauen',
    time: '2 Wochen',
    desc: 'Ich baue deinen Agenten auf n8n-Basis, verbinde ihn mit deinem Shop und trainiere ihn auf deine echten Tickets. Du bekommst Zwischenstände — nicht nur ein Endergebnis.',
  },
  {
    num: '03',
    title: 'Launch & Betrieb',
    time: 'Laufend',
    desc: 'Go-Live wird begleitet, die erste Woche engmaschig. Danach: monatliches Reporting, Anpassungen am Prompt-Verhalten und direkter Draht zu mir — kein Ticket-System.',
  },
]

export default function HowItWorks() {
  return (
    <section
      id="ablauf"
      className="section"
      style={{
        background: 'var(--bg-elevated)',
        borderTop: '1px solid var(--border)',
      }}
    >
      <div className="container">
        <div style={{ marginBottom: '3.5rem', maxWidth: '680px' }}>
          <p className="eyebrow">Ablauf</p>
          <h2 className="display-l">
            Drei Schritte.<br />
            <em style={{ color: 'var(--accent)', fontStyle: 'italic' }}>Keine Überraschungen.</em>
          </h2>
        </div>

        <ol style={{
          display: 'flex',
          flexDirection: 'column',
          gap: 0,
          listStyle: 'none',
          maxWidth: '760px',
        }}>
          {steps.map((step, i) => (
            <li
              key={step.num}
              style={{
                display: 'grid',
                gridTemplateColumns: '60px 1fr',
                gap: '1.75rem',
                paddingBottom: i < steps.length - 1 ? '2.75rem' : 0,
                position: 'relative',
              }}
            >
              <div style={{
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
              }}>
                <div style={{
                  width: '52px',
                  height: '52px',
                  borderRadius: '50%',
                  background: 'var(--bg)',
                  border: '1px solid var(--accent)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontFamily: 'var(--font-serif)',
                  fontSize: '1rem',
                  fontWeight: 500,
                  color: 'var(--accent)',
                  flexShrink: 0,
                }}>
                  {step.num}
                </div>
                {i < steps.length - 1 && (
                  <div aria-hidden="true" style={{
                    width: '1px',
                    flex: 1,
                    minHeight: '36px',
                    background: 'linear-gradient(180deg, rgba(201,166,107,0.4) 0%, rgba(201,166,107,0.05) 100%)',
                    marginTop: '0.5rem',
                  }} />
                )}
              </div>

              <div style={{ paddingTop: '0.625rem' }}>
                <div style={{
                  display: 'flex',
                  alignItems: 'baseline',
                  gap: '0.875rem',
                  marginBottom: '0.625rem',
                  flexWrap: 'wrap',
                }}>
                  <h3 style={{
                    fontFamily: 'var(--font-serif)',
                    fontSize: '1.5rem',
                    fontWeight: 500,
                    color: 'var(--text)',
                    letterSpacing: '-0.015em',
                  }}>
                    {step.title}
                  </h3>
                  <span style={{
                    fontSize: '0.75rem',
                    color: 'var(--text-subtle)',
                    letterSpacing: '0.08em',
                    textTransform: 'uppercase',
                    fontWeight: 500,
                  }}>
                    {step.time}
                  </span>
                </div>
                <p style={{
                  color: 'var(--text-muted)',
                  fontSize: '0.9375rem',
                  lineHeight: 1.7,
                  maxWidth: '560px',
                }}>
                  {step.desc}
                </p>
              </div>
            </li>
          ))}
        </ol>
      </div>
    </section>
  )
}
