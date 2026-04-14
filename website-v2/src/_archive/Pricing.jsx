import { Check } from 'lucide-react'

const plans = [
  {
    name: 'Starter',
    price: '2.000',
    period: 'einmalig',
    sub: '+ ab €490 / Monat',
    desc: 'Für Shops die automatisieren wollen ohne großes Budget.',
    features: [
      'KI-Chatbot (FAQ + Bestellstatus)',
      'Integration in dein Shopsystem',
      'Individuelle Wissensbasis',
      'Launch-Support (2 Wochen)',
      'Monatliches Reporting',
    ],
    highlight: false,
    cta: 'Jetzt starten',
  },
  {
    name: 'Professional',
    price: '5.000',
    period: 'einmalig',
    sub: '+ ab €890 / Monat',
    desc: 'Für wachsende Brands mit komplexeren Support-Anforderungen.',
    features: [
      'Alles aus Starter',
      'Automatisierte Retourenprozesse',
      'Eskalations-Workflows',
      'Mehrsprachig (DE / EN)',
      'Dedizierter Ansprechpartner',
      'Monatliche Optimierungs-Session',
    ],
    highlight: true,
    cta: 'Empfohlen — Gespräch buchen',
  },
  {
    name: 'Enterprise',
    price: 'Individuell',
    period: '',
    sub: 'Auf Anfrage',
    desc: 'Für Shops mit hohem Volumen und speziellen Anforderungen.',
    features: [
      'Alles aus Professional',
      'Custom Integrationen (ERP, WMS)',
      'Priorisierter Support',
      'SLA-Garantie',
      'White-Label Option',
    ],
    highlight: false,
    cta: 'Anfrage stellen',
  },
]

export default function Pricing() {
  return (
    <section
      id="preise"
      style={{
        padding: '6rem 1.5rem',
        background: 'linear-gradient(180deg, #0d1424 0%, #0a0f1e 100%)',
      }}
    >
      <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
        <div style={{ textAlign: 'center', marginBottom: '4rem' }}>
          <p style={{
            fontSize: '0.8rem', fontWeight: 600, letterSpacing: '0.1em',
            textTransform: 'uppercase', color: '#0284c7', marginBottom: '0.75rem',
          }}>
            Preise
          </p>
          <h2 style={{
            fontSize: 'clamp(1.75rem, 4vw, 2.75rem)',
            fontWeight: 700, color: '#f8fafc',
            letterSpacing: '-0.02em', lineHeight: 1.2, marginBottom: '1rem',
          }}>
            Transparent. Kein verstecktes Kleingedrucktes.
          </h2>
          <p style={{ color: '#94a3b8', fontSize: '1rem', maxWidth: '480px', margin: '0 auto' }}>
            Einmalige Setup-Gebühr + monatliche Betreuung. Kein Jahresvertrag im Starter-Paket.
          </p>
        </div>

        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
          gap: '1.25rem',
          alignItems: 'start',
        }}>
          {plans.map((plan) => (
            <div
              key={plan.name}
              style={{
                background: plan.highlight
                  ? 'linear-gradient(145deg, rgba(3,105,161,0.15) 0%, rgba(2,132,199,0.08) 100%)'
                  : 'rgba(255,255,255,0.03)',
                border: plan.highlight
                  ? '1px solid rgba(3,105,161,0.6)'
                  : '1px solid rgba(51,65,85,0.5)',
                borderRadius: '1.25rem',
                padding: '2rem',
                position: 'relative',
                boxShadow: plan.highlight ? '0 0 40px rgba(3,105,161,0.15)' : 'none',
              }}
            >
              {plan.highlight && (
                <div style={{
                  position: 'absolute', top: '-13px', left: '50%', transform: 'translateX(-50%)',
                  background: 'linear-gradient(135deg, #0369a1 0%, #0284c7 100%)',
                  color: '#fff', fontSize: '0.7rem', fontWeight: 700,
                  padding: '0.3rem 1rem', borderRadius: '2rem',
                  letterSpacing: '0.05em', textTransform: 'uppercase',
                  whiteSpace: 'nowrap',
                }}>
                  Meistgewählt
                </div>
              )}

              <p style={{ fontSize: '0.85rem', fontWeight: 600, color: '#0284c7', marginBottom: '0.5rem' }}>
                {plan.name}
              </p>
              <div style={{ marginBottom: '0.25rem' }}>
                <span style={{ fontSize: plan.price === 'Individuell' ? '2rem' : '2.5rem', fontWeight: 700, color: '#f8fafc', letterSpacing: '-0.02em' }}>
                  {plan.price === 'Individuell' ? plan.price : `€${plan.price}`}
                </span>
                {plan.period && (
                  <span style={{ color: '#94a3b8', fontSize: '0.85rem', marginLeft: '0.4rem' }}>
                    {plan.period}
                  </span>
                )}
              </div>
              <p style={{ color: '#0284c7', fontSize: '0.8rem', fontWeight: 500, marginBottom: '0.75rem' }}>
                {plan.sub}
              </p>
              <p style={{ color: '#94a3b8', fontSize: '0.875rem', lineHeight: 1.6, marginBottom: '1.75rem' }}>
                {plan.desc}
              </p>

              <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '0.6rem', marginBottom: '2rem' }}>
                {plan.features.map((f) => (
                  <li key={f} style={{ display: 'flex', alignItems: 'flex-start', gap: '0.6rem', fontSize: '0.875rem', color: '#cbd5e1' }}>
                    <Check size={16} color="#0284c7" style={{ flexShrink: 0, marginTop: '2px' }} />
                    {f}
                  </li>
                ))}
              </ul>

              <a
                href="#kontakt"
                style={{
                  display: 'block', textAlign: 'center',
                  background: plan.highlight
                    ? 'linear-gradient(135deg, #0369a1 0%, #0284c7 100%)'
                    : 'rgba(255,255,255,0.06)',
                  border: plan.highlight ? 'none' : '1px solid rgba(255,255,255,0.12)',
                  color: '#fff',
                  padding: '0.8rem 1.5rem',
                  borderRadius: '0.625rem',
                  fontSize: '0.875rem',
                  fontWeight: 600,
                  textDecoration: 'none',
                  transition: 'opacity 0.2s ease, transform 0.2s ease',
                  boxShadow: plan.highlight ? '0 4px 20px rgba(3,105,161,0.35)' : 'none',
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.opacity = '0.88'
                  e.currentTarget.style.transform = 'translateY(-1px)'
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.opacity = '1'
                  e.currentTarget.style.transform = 'translateY(0)'
                }}
              >
                {plan.cta}
              </a>
            </div>
          ))}
        </div>

        <p style={{ textAlign: 'center', color: '#475569', fontSize: '0.8rem', marginTop: '2rem' }}>
          Alle Preise zzgl. MwSt. · Kleinunternehmer § 19 UStG
        </p>
      </div>
    </section>
  )
}
