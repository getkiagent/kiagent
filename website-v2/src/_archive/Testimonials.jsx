import { Quote } from 'lucide-react'

const testimonials = [
  {
    quote: 'Seit wir GetKiAgent einsetzen, bearbeiten wir 60% weniger Support-Tickets manuell. Das Team kann sich endlich auf wichtigere Dinge konzentrieren.',
    name: 'Sarah M.',
    role: 'Head of E-Commerce',
    shop: 'Beauty Brand, Düsseldorf',
    initials: 'SM',
  },
  {
    quote: 'Setup war innerhalb von 2 Wochen abgeschlossen. Die Qualität der automatischen Antworten hat unsere Kunden überrascht — positiv.',
    name: 'Thomas K.',
    role: 'Gründer',
    shop: 'Supplement Shop, München',
    initials: 'TK',
  },
  {
    quote: 'Endlich kein Ticket-Chaos mehr an Wochenenden. Der KI-Agent gibt sofort Antworten — auch auf Englisch.',
    name: 'Lisa H.',
    role: 'Operations Manager',
    shop: 'Skincare DTC, Wien',
    initials: 'LH',
  },
]

const stats = [
  { value: '60%', label: 'weniger manuelle Tickets' },
  { value: '24/7', label: 'Verfügbarkeit' },
  { value: '2 Wo.', label: 'bis Go-Live' },
  { value: '< 5s', label: 'Antwortzeit' },
]

export default function Testimonials() {
  return (
    <section
      style={{
        padding: '6rem 1.5rem',
        background: '#0a0f1e',
      }}
    >
      <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
        {/* Stats bar */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))',
          gap: '1px',
          background: 'rgba(51,65,85,0.4)',
          border: '1px solid rgba(51,65,85,0.4)',
          borderRadius: '1rem',
          overflow: 'hidden',
          marginBottom: '5rem',
        }}>
          {stats.map((s) => (
            <div key={s.label} style={{
              background: 'rgba(10,15,30,0.9)',
              padding: '1.75rem 1.5rem',
              textAlign: 'center',
            }}>
              <div style={{ fontSize: '2rem', fontWeight: 700, color: '#0284c7', letterSpacing: '-0.03em' }}>
                {s.value}
              </div>
              <div style={{ color: '#94a3b8', fontSize: '0.8rem', marginTop: '0.25rem' }}>
                {s.label}
              </div>
            </div>
          ))}
        </div>

        {/* Section header */}
        <div style={{ textAlign: 'center', marginBottom: '3rem' }}>
          <p style={{
            fontSize: '0.8rem', fontWeight: 600, letterSpacing: '0.1em',
            textTransform: 'uppercase', color: '#0284c7', marginBottom: '0.75rem',
          }}>
            Kundenstimmen
          </p>
          <h2 style={{
            fontSize: 'clamp(1.75rem, 4vw, 2.75rem)',
            fontWeight: 700, color: '#f8fafc',
            letterSpacing: '-0.02em', lineHeight: 1.2,
          }}>
            Was unsere Kunden sagen
          </h2>
        </div>

        {/* Cards */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
          gap: '1.25rem',
        }}>
          {testimonials.map((t) => (
            <div
              key={t.name}
              style={{
                background: 'rgba(255,255,255,0.03)',
                border: '1px solid rgba(51,65,85,0.5)',
                borderRadius: '1rem',
                padding: '2rem',
                display: 'flex',
                flexDirection: 'column',
                gap: '1.5rem',
              }}
            >
              <Quote size={24} color="rgba(3,105,161,0.5)" />
              <p style={{ color: '#cbd5e1', fontSize: '0.95rem', lineHeight: 1.7, flex: 1 }}>
                "{t.quote}"
              </p>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.875rem' }}>
                <div style={{
                  width: '40px', height: '40px', borderRadius: '50%',
                  background: 'linear-gradient(135deg, #0369a1 0%, #0284c7 100%)',
                  display: 'flex', alignItems: 'center', justifyContent: 'center',
                  fontSize: '0.75rem', fontWeight: 700, color: '#fff',
                  flexShrink: 0,
                }}>
                  {t.initials}
                </div>
                <div>
                  <div style={{ fontWeight: 600, fontSize: '0.875rem', color: '#f1f5f9' }}>{t.name}</div>
                  <div style={{ fontSize: '0.775rem', color: '#94a3b8' }}>{t.role} · {t.shop}</div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
