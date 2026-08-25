import React, { useState, useEffect } from 'react';
import { ArrowRight, FileText } from 'lucide-react';

export const Navbar: React.FC = () => {
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 20);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const scrollToWorkspace = () => {
    document.getElementById('docstyle-workspace')?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <header
      id="navbar-header"
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        scrolled
          ? 'bg-[#F4EFEA]/90 backdrop-blur-md shadow-xs py-3.5'
          : 'bg-[#F4EFEA] py-5'
      }`}
    >
      <div className="max-w-7xl mx-auto px-6 sm:px-8 lg:px-12 flex items-center justify-between">
        <nav className="hidden lg:flex items-center gap-7 text-[13px] font-medium text-[#1A1A1A]">
          <button
            onClick={scrollToWorkspace}
            className="hover:opacity-60 transition-opacity cursor-pointer"
          >
            Restyler Workspace
          </button>
          <a
            href="#features"
            className="hover:opacity-60 transition-opacity"
          >
            Features
          </a>
        </nav>

        <div className="flex-1 lg:flex-initial text-left lg:text-center">
          <a
            id="brand-logo"
            href="#"
            className="text-xl sm:text-2xl font-extrabold tracking-tight text-[#1A1A1A] font-sans-clean inline-flex items-center gap-2"
          >
            <FileText className="w-5 h-5 text-[#111111]" />
            DocStyle Engine
          </a>
        </div>

        <div className="hidden lg:flex items-center gap-7 text-[13px] font-medium text-[#1A1A1A]">
          <button
            id="btn-get-started-nav"
            onClick={scrollToWorkspace}
            className="bg-[#111111] hover:bg-black text-white px-5 py-2 rounded-full text-xs font-semibold flex items-center gap-1.5 transition-transform hover:scale-105 active:scale-95 cursor-pointer"
          >
            <span>Start Restyling</span>
            <ArrowRight className="w-3 h-3" />
          </button>
        </div>

        <div className="flex lg:hidden items-center gap-3">
          <button
            id="btn-mobile-cta-top"
            onClick={scrollToWorkspace}
            className="bg-[#111111] text-white px-3.5 py-1.5 rounded-full text-xs font-medium flex items-center gap-1"
          >
            <span>Start</span>
            <ArrowRight className="w-2.5 h-2.5" />
          </button>
        </div>
      </div>
    </header>
  );
};
