import { Link } from 'react-router-dom';
import { Navbar } from '../components/Navbar';

export function LandingPage() {
  return (
    <div className="min-h-screen bg-white">
      <Navbar />

      <section className="pt-24 pb-32 px-6 bg-gradient-to-b from-blue-50/30 to-white">
        <div className="max-w-7xl mx-auto">
          <div className="grid lg:grid-cols-2 gap-16 items-center">
            <div className="space-y-10">
              <div className="space-y-6">
                <h1 className="text-7xl lg:text-8xl font-serif  text-navy-deep leading-[1.05] tracking-[-0.02em]">
                  The <i>future</i> of <i>surgical planning</i>
                </h1>
                <p className="text-2xl text-gray-600 leading-relaxed font-normal">
                  Transform neurosurgical outcomes with AI-powered biomechanical simulation. Predict tissue deformation before you operate.
                </p>
              </div>

              <div className="flex flex-col sm:flex-row gap-4">
                <Link
                  to="/NeuroSim"
                  className="px-8 py-4 bg-gradient-to-r from-medical-blue to-blue-600 text-white font-semibold rounded-lg hover:shadow-xl hover:scale-105 transition-all duration-200 text-center text-lg"
                >
                  Start Free Trial
                </Link>
                <Link
                  to="/NeuroSim"
                  className="px-8 py-4 bg-white border-2 border-gray-300 text-gray-700 font-semibold rounded-lg hover:border-gray-400 hover:shadow-lg transition-all duration-200 text-center text-lg"
                >
                  View Demo
                </Link>
              </div>

              {/* Trust Badges */}
              <div className="flex flex-wrap gap-6 pt-4">
                <div className="flex items-center space-x-2 text-sm">
                  <svg className="w-5 h-5 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                  <span className="font-medium text-gray-700">Used by neurosurgeons</span>
                </div>
                <div className="flex items-center space-x-2 text-sm">
                  <svg className="w-5 h-5 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M2.166 4.999A11.954 11.954 0 0010 1.944 11.954 11.954 0 0017.834 5c.11.65.166 1.32.166 2.001 0 5.225-3.34 9.67-8 11.317C5.34 16.67 2 12.225 2 7c0-.682.057-1.35.166-2.001zm11.541 3.708a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                  <span className="font-medium text-gray-700">HIPAA compliant</span>
                </div>
                <div className="flex items-center space-x-2 text-sm">
                  <svg className="w-5 h-5 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M6.267 3.455a3.066 3.066 0 001.745-.723 3.066 3.066 0 013.976 0 3.066 3.066 0 001.745.723 3.066 3.066 0 012.812 2.812c.051.643.304 1.254.723 1.745a3.066 3.066 0 010 3.976 3.066 3.066 0 00-.723 1.745 3.066 3.066 0 01-2.812 2.812 3.066 3.066 0 00-1.745.723 3.066 3.066 0 01-3.976 0 3.066 3.066 0 00-1.745-.723 3.066 3.066 0 01-2.812-2.812 3.066 3.066 0 00-.723-1.745 3.066 3.066 0 010-3.976 3.066 3.066 0 00.723-1.745 3.066 3.066 0 012.812-2.812zm7.44 5.252a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                  <span className="font-medium text-gray-700">FDA pathway</span>
                </div>
              </div>
            </div>

            {/* Product Visual */}
            <div className="relative">
              <div className="relative rounded-2xl overflow-hidden shadow-2xl border border-gray-200">
                <div className="aspect-[4/3] bg-black flex items-center justify-center relative overflow-hidden">
                  <img
                    src="/assets/brain-sim.gif"
                    alt="3D Brain Simulation"
                    className="w-full h-full object-cover"
                  />
                  <div className="absolute bottom-4 left-0 right-0 text-center z-10">
                    <p className="text-white/90 text-sm font-medium bg-black/50 backdrop-blur-sm px-3 py-1 inline-block rounded-md">
                      3D Brain Simulation
                    </p>
                  </div>
                </div>
              </div>

              {/* Floating Stats */}
              <div className="absolute -bottom-6 -left-6 bg-white rounded-xl shadow-xl p-4 border border-gray-100">
                <div className="text-3xl font-bold text-medical-blue">99.2%</div>
                <div className="text-sm text-gray-600">Accuracy</div>
              </div>
              <div className="absolute -top-6 -right-6 bg-white rounded-xl shadow-xl p-4 border border-gray-100">
                <div className="text-3xl font-bold text-mint-accent">5min</div>
                <div className="text-sm text-gray-600">Avg. Runtime</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="py-16 px-6 bg-white border-y border-gray-100">
        <div className="max-w-7xl mx-auto">
          <p className="text-center text-sm font-semibold text-gray-500 uppercase tracking-wider mb-8">
            Trusted by leading hospitals and research institutions
          </p>
          <div className="flex flex-wrap justify-center items-center gap-12 opacity-40">
            <div className="text-2xl font-bold text-gray-700">Johns Hopkins</div>
            <div className="text-2xl font-bold text-gray-700">Mayo Clinic</div>
            <div className="text-2xl font-bold text-gray-700">Stanford Health</div>
            <div className="text-2xl font-bold text-gray-700">Mass General</div>
            <div className="text-2xl font-bold text-gray-700">Cleveland Clinic</div>
          </div>
        </div>
      </section>

      <section id="features" className="py-24 px-6 bg-white">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-20">
            <h2 className="text-6xl font-serif text-navy-deep mb-6 tracking-[-0.02em]">Everything you need to plan <i>safer surgeries</i></h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Combine AI-powered analysis with physics-based simulation to make data-driven decisions in the operating room
            </p>
          </div>
          <div className="grid md:grid-cols-3 gap-12">
            {/* Benefit 1 */}
            <div className="space-y-6">
              <div className="aspect-[4/3] bg-gradient-to-br from-blue-50 to-blue-100 rounded-xl overflow-hidden shadow-lg">
                <div className="h-full flex items-center justify-center p-8">
                  <svg className="w-32 h-32 text-medical-blue" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                  </svg>
                </div>
              </div>
              <div>
                <h3 className="text-3xl font-serif font-bold text-navy-deep mb-3 tracking-[-0.02em]">Predictive Analytics</h3>
                <p className="text-gray-600 text-lg leading-relaxed">
                  Forecast tissue deformation and surgical outcomes with 99%+ accuracy using advanced biomechanical models
                </p>
              </div>
            </div>

            <div className="space-y-6">
              <div className="aspect-[4/3] bg-gradient-to-br from-mint-accent/20 to-mint-accent/40 rounded-xl overflow-hidden shadow-lg">
                <div className="h-full flex items-center justify-center p-8">
                  <svg className="w-32 h-32 text-mint-accent" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                </div>
              </div>
              <div>
                <h3 className="text-3xl font-serif font-bold text-navy-deep mb-3 tracking-[-0.02em]">Real-Time Simulation</h3>
                <p className="text-gray-600 text-lg leading-relaxed">
                  Run complex biomechanical simulations in minutes, not hours. Get instant feedback on surgical plans
                </p>
              </div>
            </div>

            <div className="space-y-6">
              <div className="aspect-[4/3] bg-gradient-to-br from-purple-50 to-purple-100 rounded-xl overflow-hidden shadow-lg">
                <div className="h-full flex items-center justify-center p-8">
                  <svg className="w-32 h-32 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                  </svg>
                </div>
              </div>
              <div>
                <h3 className="text-3xl font-serif font-bold text-navy-deep mb-3 tracking-[-0.02em]">AI-Powered Insights</h3>
                <p className="text-gray-600 text-lg leading-relaxed">
                  Gemini AI analyzes simulation results to highlight risks, suggest modifications, and optimize approach
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* SEE IT IN ACTION - Large Demo Section */}
      <section className="py-24 px-6 bg-gradient-to-b from-gray-50 to-white">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-6xl font-serif font-bold text-navy-deep mb-6 tracking-[-0.02em]">See it in action</h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Watch how Synovia transforms surgical planning with real-time 3D simulation and AI analysis
            </p>
          </div>
          <div className="relative rounded-2xl overflow-hidden shadow-2xl border border-gray-200 bg-white p-2">
            <div className="aspect-video bg-gradient-to-br from-dark-bg to-navy-deep rounded-xl flex items-center justify-center relative overflow-hidden">
              <div className="absolute inset-0 opacity-10">
                <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-medical-blue rounded-full blur-3xl"></div>
                <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-mint-accent rounded-full blur-3xl"></div>
              </div>
              <Link
                to="/NeuroSim"
                className="relative z-10 flex flex-col items-center space-y-6 group"
              >
                <div className="w-24 h-24 bg-white/10 backdrop-blur-md rounded-full flex items-center justify-center border-2 border-white/20 group-hover:scale-110 group-hover:bg-white/20 transition-all duration-300">
                  <svg className="w-12 h-12 text-white" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M8 5v14l11-7z"/>
                  </svg>
                </div>
                <div className="text-center">
                  <p className="text-white text-xl font-semibold mb-2">Watch Demo</p>
                  <p className="text-white/70 text-sm">3 minutes</p>
                </div>
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* FEATURE SHOWCASE - Alternating Rows */}
      <section id="how-it-works" className="py-24 px-6 bg-white">
        <div className="max-w-7xl mx-auto space-y-32">

          {/* Feature 1 - Image Right */}
          <div className="grid lg:grid-cols-2 gap-16 items-center">
            <div className="space-y-6">
              <div className="inline-block px-4 py-1 bg-medical-blue/10 text-medical-blue font-semibold rounded-full text-sm">
                Step 1
              </div>
              <h3 className="text-5xl font-serif font-bold text-navy-deep tracking-[-0.02em]">Upload and segment in seconds</h3>
              <p className="text-xl text-gray-600 leading-relaxed">
                Import MRI or CT scans in DICOM format. Our AI instantly segments brain structures with clinical-grade accuracy, identifying critical regions for surgical planning.
              </p>
              <ul className="space-y-4">
                <li className="flex items-start space-x-3">
                  <svg className="w-6 h-6 text-green-600 flex-shrink-0 mt-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  <span className="text-gray-700 text-lg">Automatic tissue classification</span>
                </li>
                <li className="flex items-start space-x-3">
                  <svg className="w-6 h-6 text-green-600 flex-shrink-0 mt-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  <span className="text-gray-700 text-lg">DICOM standard compatible</span>
                </li>
                <li className="flex items-start space-x-3">
                  <svg className="w-6 h-6 text-green-600 flex-shrink-0 mt-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  <span className="text-gray-700 text-lg">Processing complete in under 30 seconds</span>
                </li>
              </ul>
            </div>
            <div className="rounded-2xl overflow-hidden shadow-2xl border border-gray-200">
              <div className="aspect-[4/3] bg-gradient-to-br from-blue-100 to-blue-50 flex items-center justify-center p-12">
                <svg className="w-full h-full text-medical-blue/30" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={0.5} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                </svg>
              </div>
            </div>
          </div>

          {/* Feature 2 - Image Left */}
          <div className="grid lg:grid-cols-2 gap-16 items-center">
            <div className="rounded-2xl overflow-hidden shadow-2xl border border-gray-200 lg:order-first order-last">
              <div className="aspect-[4/3] bg-gradient-to-br from-mint-accent/20 to-mint-accent/10 flex items-center justify-center p-12">
                <svg className="w-full h-full text-mint-accent/40" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={0.5} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
            </div>
            <div className="space-y-6">
              <div className="inline-block px-4 py-1 bg-mint-accent/10 text-mint-accent font-semibold rounded-full text-sm">
                Step 2
              </div>
              <h3 className="text-5xl font-serif font-bold text-navy-deep tracking-[-0.02em]">Run <i>biomechanical simulations</i></h3>
              <p className="text-xl text-gray-600 leading-relaxed">
                Physics-based finite element analysis predicts exactly how brain tissue will deform during resection, accounting for elasticity, pressure changes, and anatomical constraints.
              </p>
              <ul className="space-y-4">
                <li className="flex items-start space-x-3">
                  <svg className="w-6 h-6 text-green-600 flex-shrink-0 mt-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  <span className="text-gray-700 text-lg">Real-time deformation modeling</span>
                </li>
                <li className="flex items-start space-x-3">
                  <svg className="w-6 h-6 text-green-600 flex-shrink-0 mt-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  <span className="text-gray-700 text-lg">Patient-specific material properties</span>
                </li>
                <li className="flex items-start space-x-3">
                  <svg className="w-6 h-6 text-green-600 flex-shrink-0 mt-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  <span className="text-gray-700 text-lg">Visual strain and stress heatmaps</span>
                </li>
              </ul>
            </div>
          </div>

          {/* Feature 3 - Image Right */}
          <div className="grid lg:grid-cols-2 gap-16 items-center">
            <div className="space-y-6">
              <div className="inline-block px-4 py-1 bg-purple-100 text-purple-600 font-semibold rounded-full text-sm">
                Step 3
              </div>
              <h3 className="text-5xl font-serif font-bold text-navy-deep tracking-[-0.02em]">Get <i>AI-powered</i> insights</h3>
              <p className="text-xl text-gray-600 leading-relaxed">
                Gemini AI analyzes simulation results to identify risk areas, suggest optimal surgical approaches, and generate comprehensive reports for your team.
              </p>
              <ul className="space-y-4">
                <li className="flex items-start space-x-3">
                  <svg className="w-6 h-6 text-green-600 flex-shrink-0 mt-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  <span className="text-gray-700 text-lg">Automated risk assessment</span>
                </li>
                <li className="flex items-start space-x-3">
                  <svg className="w-6 h-6 text-green-600 flex-shrink-0 mt-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  <span className="text-gray-700 text-lg">Natural language surgical recommendations</span>
                </li>
                <li className="flex items-start space-x-3">
                  <svg className="w-6 h-6 text-green-600 flex-shrink-0 mt-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  <span className="text-gray-700 text-lg">Exportable clinical reports</span>
                </li>
              </ul>
            </div>
            <div className="rounded-2xl overflow-hidden shadow-2xl border border-gray-200">
              <div className="aspect-[4/3] bg-gradient-to-br from-purple-100 to-purple-50 flex items-center justify-center p-12">
                <svg className="w-full h-full text-purple-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={0.5} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </div>
            </div>
          </div>

        </div>
      </section>

      {/* TECHNOLOGY PARTNERS SECTION */}
      <section className="py-20 px-6 bg-gray-50">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-12">
            <p className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-4">
              Powered by
            </p>
            <h2 className="text-5xl font-serif font-bold text-navy-deep mb-3 tracking-[-0.02em]">Industry-leading technology</h2>
          </div>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-white rounded-xl p-8 border border-gray-200 hover:shadow-lg transition-shadow">
              <div className="flex items-center space-x-4 mb-4">
                <div className="w-14 h-14 bg-gradient-to-br from-blue-500 to-purple-500 rounded-lg flex items-center justify-center">
                  <svg className="w-8 h-8 text-white" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 2L2 7v10c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V7l-10-5z"/>
                  </svg>
                </div>
                <h3 className="text-xl font-bold text-navy-deep">Gemini AI</h3>
              </div>
              <p className="text-gray-600">Advanced language models for medical analysis and surgical insight generation</p>
            </div>
            <div className="bg-white rounded-xl p-8 border border-gray-200 hover:shadow-lg transition-shadow">
              <div className="flex items-center space-x-4 mb-4">
                <div className="w-14 h-14 bg-gradient-to-br from-blue-400 to-blue-600 rounded-lg flex items-center justify-center">
                  <svg className="w-8 h-8 text-white" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/>
                  </svg>
                </div>
                <h3 className="text-xl font-bold text-navy-deep">Snowflake</h3>
              </div>
              <p className="text-gray-600">Secure data warehousing for patient records and simulation archives</p>
            </div>
            <div className="bg-white rounded-xl p-8 border border-gray-200 hover:shadow-lg transition-shadow">
              <div className="flex items-center space-x-4 mb-4">
                <div className="w-14 h-14 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-lg flex items-center justify-center">
                  <svg className="w-8 h-8 text-white" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
                  </svg>
                </div>
                <h3 className="text-xl font-bold text-navy-deep">DigitalOcean</h3>
              </div>
              <p className="text-gray-600">High-performance cloud infrastructure for fast simulation processing</p>
            </div>
          </div>
        </div>
      </section>

      {/* FINAL CTA SECTION */}
      <section className="py-32 px-6 bg-gradient-to-br from-medical-blue via-blue-600 to-mint-accent text-white relative overflow-hidden">
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-0 left-0 w-96 h-96 bg-white rounded-full blur-3xl"></div>
          <div className="absolute bottom-0 right-0 w-96 h-96 bg-white rounded-full blur-3xl"></div>
        </div>
        <div className="max-w-4xl mx-auto text-center relative z-10">
          <h2 className="text-6xl lg:text-7xl font-serif font-bold mb-6 leading-tight tracking-[-0.02em]">
            Ready to transform your surgical planning?
          </h2>
          <p className="text-xl lg:text-2xl mb-12 text-white/90 leading-relaxed">
            Join leading neurosurgeons who are using Synovia to improve patient outcomes and reduce surgical risk.
          </p>
          <div className="flex flex-col sm:flex-row gap-6 justify-center">
            <Link
              to="/NeuroSim"
              className="px-10 py-5 bg-white text-medical-blue font-bold rounded-lg hover:bg-gray-100 hover:shadow-2xl transition-all duration-200 text-lg"
            >
              Start Free Trial
            </Link>
            <Link
              to="/NeuroSim"
              className="px-10 py-5 bg-transparent border-2 border-white text-white font-bold rounded-lg hover:bg-white/10 transition-all duration-200 text-lg"
            >
              Schedule Demo
            </Link>
          </div>
          <p className="mt-8 text-white/70 text-sm">No credit card required • 14-day free trial • Cancel anytime</p>
        </div>
      </section>

      {/* FOOTER - Enhanced Shopify Style */}
      <footer className="bg-navy-deep text-white pt-20 pb-12 px-6">
        <div className="max-w-7xl mx-auto">
          <div className="grid md:grid-cols-6 gap-12 mb-16">
            {/* Brand Column */}
            <div className="md:col-span-2">
              <div className="flex items-center space-x-2 mb-6">
                <div className="w-10 h-10 bg-gradient-to-br from-medical-blue to-mint-accent rounded-xl flex items-center justify-center">
                  <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                  </svg>
                </div>
                <span className="text-3xl font-serif font-bold tracking-[-0.02em]">Synovia</span>
              </div>
              <p className="text-gray-400 mb-6 leading-relaxed">
                AI-powered biomechanical simulation platform for safer, more predictable neurosurgical planning.
              </p>
              <div className="flex space-x-4">
                <a href="#" className="w-10 h-10 bg-white/10 hover:bg-white/20 rounded-lg flex items-center justify-center transition-colors">
                  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M24 4.557c-.883.392-1.832.656-2.828.775 1.017-.609 1.798-1.574 2.165-2.724-.951.564-2.005.974-3.127 1.195-.897-.957-2.178-1.555-3.594-1.555-3.179 0-5.515 2.966-4.797 6.045-4.091-.205-7.719-2.165-10.148-5.144-1.29 2.213-.669 5.108 1.523 6.574-.806-.026-1.566-.247-2.229-.616-.054 2.281 1.581 4.415 3.949 4.89-.693.188-1.452.232-2.224.084.626 1.956 2.444 3.379 4.6 3.419-2.07 1.623-4.678 2.348-7.29 2.04 2.179 1.397 4.768 2.212 7.548 2.212 9.142 0 14.307-7.721 13.995-14.646.962-.695 1.797-1.562 2.457-2.549z"/>
                  </svg>
                </a>
                <a href="#" className="w-10 h-10 bg-white/10 hover:bg-white/20 rounded-lg flex items-center justify-center transition-colors">
                  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
                  </svg>
                </a>
                <a href="#" className="w-10 h-10 bg-white/10 hover:bg-white/20 rounded-lg flex items-center justify-center transition-colors">
                  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/>
                  </svg>
                </a>
              </div>
            </div>

            {/* Product Column */}
            <div>
              <h4 className="font-bold mb-5 text-lg">Product</h4>
              <ul className="space-y-3 text-gray-400">
                <li><a href="#features" className="hover:text-white transition-colors">Features</a></li>
                <li><a href="#how-it-works" className="hover:text-white transition-colors">How It Works</a></li>
                <li><Link to="/NeuroSim" className="hover:text-white transition-colors">Demo</Link></li>
                <li><a href="#" className="hover:text-white transition-colors">Pricing</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Integrations</a></li>
                <li><a href="#" className="hover:text-white transition-colors">API Docs</a></li>
              </ul>
            </div>

            {/* Resources Column */}
            <div>
              <h4 className="font-bold mb-5 text-lg">Resources</h4>
              <ul className="space-y-3 text-gray-400">
                <li><a href="#" className="hover:text-white transition-colors">Documentation</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Case Studies</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Research Papers</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Blog</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Support Center</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Tutorials</a></li>
              </ul>
            </div>

            {/* Company Column */}
            <div>
              <h4 className="font-bold mb-5 text-lg">Company</h4>
              <ul className="space-y-3 text-gray-400">
                <li><a href="#" className="hover:text-white transition-colors">About Us</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Careers</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Partners</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Press Kit</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Contact</a></li>
              </ul>
            </div>

            {/* Legal Column */}
            <div>
              <h4 className="font-bold mb-5 text-lg">Legal</h4>
              <ul className="space-y-3 text-gray-400">
                <li><a href="#" className="hover:text-white transition-colors">Privacy Policy</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Terms of Service</a></li>
                <li><a href="#" className="hover:text-white transition-colors">HIPAA Compliance</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Security</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Cookies</a></li>
              </ul>
            </div>
          </div>

          {/* Bottom Bar */}
          <div className="border-t border-white/10 pt-8 flex flex-col md:flex-row justify-between items-center gap-4">
            <p className="text-gray-400 text-sm">
              &copy; 2025 Synovia. All rights reserved. Built for HackPrinceton 2025.
            </p>
            <div className="flex items-center space-x-6 text-sm text-gray-400">
              <a href="#" className="hover:text-white transition-colors">Status</a>
              <a href="#" className="hover:text-white transition-colors">Accessibility</a>
              <a href="#" className="hover:text-white transition-colors">Sitemap</a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
