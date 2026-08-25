import React from 'react';
import { Navbar } from './components/Navbar';
import { Hero } from './components/Hero';
import { DocStyleWorkspace } from './components/DocStyleWorkspace';
import { FeatureGrid } from './components/FeatureGrid';
import { ImpactShowcase } from './components/ImpactShowcase';
import { Footer } from './components/Footer';

export default function App() {
  return (
    <div id="docstyle-app" className="min-h-screen bg-[#F4EFEA] text-[#1A1A1A] flex flex-col font-sans-clean selection:bg-[#1A1A1A] selection:text-white">
      {/* Top Navbar */}
      <Navbar />

      {/* Main Content Area */}
      <main className="flex-1 w-full">
        {/* Hero Section */}
        <Hero />

        {/* DocStyle Interactive Workspace */}
        <DocStyleWorkspace />

        {/* Feature Grid Section with Project Images */}
        <FeatureGrid />

        {/* Impact Showcase Section */}
        <ImpactShowcase />
      </main>

      {/* Footer */}
      <Footer />
    </div>
  );
}
