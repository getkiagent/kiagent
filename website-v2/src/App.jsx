import './index.css'
import Nav from './components/Nav'
import Hero from './components/Hero'
import Features from './components/Features'
import HowItWorks from './components/HowItWorks'
import Credibility from './components/Credibility'
import Contact from './components/Contact'
import Footer from './components/Footer'

function App() {
  return (
    <>
      <a href="#main" className="skip-link">Zum Inhalt springen</a>
      <Nav />
      <main id="main">
        <Hero />
        <Features />
        <HowItWorks />
        <Credibility />
        <Contact />
      </main>
      <Footer />
    </>
  )
}

export default App
