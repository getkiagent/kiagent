import './index.css'
import Nav from './components/Nav'
import Hero from './components/Hero'
import Pain from './components/Pain'
import Features from './components/Features'
import CaseStudy from './components/CaseStudy'
import HowItWorks from './components/HowItWorks'
import Products from './components/Products'
import Pricing from './components/Pricing'
import Credibility from './components/Credibility'
import Rechner from './components/Rechner'
import FAQ from './components/FAQ'
import Contact from './components/Contact'
import Footer from './components/Footer'
import StickyCtaMobile from './components/StickyCtaMobile'

function App() {
  return (
    <>
      <a href="#main" className="skip-link">Zum Inhalt springen</a>
      <Nav />
      <main id="main">
        <Hero />
        <Pain />
        <Features />
        <CaseStudy />
        <HowItWorks />
        <Products />
        <Pricing />
        <Credibility />
        <Rechner />
        <FAQ />
        <Contact />
      </main>
      <Footer />
      <StickyCtaMobile />
    </>
  )
}

export default App
