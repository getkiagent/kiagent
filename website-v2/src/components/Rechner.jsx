import { useState, useMemo } from 'react'

function fmt(n) {
  return n.toLocaleString('de-DE', { style: 'currency', currency: 'EUR', maximumFractionDigits: 0 })
}

export default function Rechner() {
  const [tickets, setTickets] = useState(300)
  const [avgMin, setAvgMin] = useState(8)
  const [hourlyRate, setHourlyRate] = useState(20)

  const results = useMemo(() => {
    const hoursTotal = (tickets * avgMin) / 60
    const currentCost = hoursTotal * hourlyRate
    const retainer = tickets <= 400 ? 190 : 390
    const agentCost = hoursTotal * 0.35 * hourlyRate + retainer
    const saving = currentCost - agentCost
    return { currentCost, agentCost, saving: Math.max(saving, 0), retainer }
  }, [tickets, avgMin, hourlyRate])

  const sliders = [
    { label: 'Tickets / Monat', value: tickets, min: 50, max: 2000, step: 50, set: setTickets, unit: '' },
    { label: 'Ø Bearbeitungszeit', value: avgMin, min: 2, max: 30, step: 1, set: setAvgMin, unit: ' Min' },
    { label: 'Stundensatz Mitarbeiter', value: hourlyRate, min: 12, max: 50, step: 1, set: setHourlyRate, unit: ' €/h' },
  ]

  return (
    <section
      id="rechner"
      className="section"
      style={{
        background: 'var(--bg)',
        borderTop: '1px solid var(--border)',
      }}
    >
      <div className="container">
        <div style={{ marginBottom: '3rem', maxWidth: '680px' }}>
          <p className="eyebrow">Ticket-Kosten-Rechner</p>
          <h2 className="display-l" style={{ marginBottom: '1rem' }}>
            Was kostet dein Support<br />
            <em style={{ color: 'var(--accent)', fontStyle: 'italic' }}>wirklich?</em>
          </h2>
          <p className="lead">Stell deine Zahlen ein — und sieh, was Automatisierung konkret spart.</p>
        </div>

        <div style={{
          display: 'grid',
          gridTemplateColumns: 'minmax(0, 1fr) minmax(0, 1fr)',
          gap: '3rem',
          alignItems: 'start',
        }}>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
            {sliders.map(({ label, value, min, max, step, set, unit }) => (
              <div key={label}>
                <div style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  marginBottom: '0.625rem',
                }}>
                  <label style={{ fontSize: '0.875rem', color: 'var(--text-muted)', fontWeight: 500 }}>
                    {label}
                  </label>
                  <span style={{
                    fontFamily: 'var(--font-serif)',
                    fontSize: '1rem',
                    fontWeight: 500,
                    color: 'var(--text)',
                  }}>
                    {value}{unit}
                  </span>
                </div>
                <input
                  type="range"
                  min={min}
                  max={max}
                  step={step}
                  value={value}
                  onChange={(e) => set(Number(e.target.value))}
                  style={{
                    width: '100%',
                    accentColor: 'var(--accent)',
                    cursor: 'pointer',
                  }}
                />
              </div>
            ))}
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            {[
              { label: 'Aktuelle Support-Kosten (Arbeitszeit)', value: results.currentCost, highlight: false },
              { label: `Mit GetKiAgent (65 % automatisiert + €${results.retainer}/Mo Retainer)`, value: results.agentCost, highlight: false },
              { label: 'Monatliche Ersparnis', value: results.saving, highlight: true },
            ].map(({ label, value, highlight }) => (
              <div
                key={label}
                style={{
                  background: highlight ? 'rgba(201, 166, 107, 0.07)' : 'var(--bg-elevated)',
                  border: highlight ? '1px solid rgba(201, 166, 107, 0.35)' : '1px solid var(--border)',
                  borderRadius: 'var(--r-md)',
                  padding: '1.25rem 1.5rem',
                }}
              >
                <div style={{ fontSize: '0.75rem', color: 'var(--text-subtle)', marginBottom: '0.375rem', lineHeight: 1.4 }}>
                  {label}
                </div>
                <div style={{
                  fontFamily: 'var(--font-serif)',
                  fontSize: 'clamp(1.5rem, 2.5vw, 2rem)',
                  fontWeight: 500,
                  color: highlight ? 'var(--accent)' : 'var(--text)',
                  letterSpacing: '-0.025em',
                  lineHeight: 1,
                }}>
                  {fmt(value)}
                </div>
              </div>
            ))}
            <p style={{ fontSize: '0.72rem', color: 'var(--text-subtle)', lineHeight: 1.6 }}>
              Basiert auf Arbeitszeit-Kosten. Setup-Gebühr nicht eingerechnet. Tatsächliche Automatisierungsrate variiert je nach Ticket-Mix.
            </p>
            <a
              href="#kontakt"
              className="btn-primary"
              style={{ textAlign: 'center', justifyContent: 'center' }}
            >
              Diese Zahlen für mein Team prüfen
            </a>
          </div>
        </div>
      </div>
    </section>
  )
}
