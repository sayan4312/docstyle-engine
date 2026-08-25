import React from 'react';
import { ArrowRight, FileText, Play } from 'lucide-react';
import { TeamGallery } from './TeamGallery';
import { HeroFeatures } from './HeroFeatures';

export const Hero: React.FC = () => {
  const scrollToWorkspace = () => {
    document.getElementById('docstyle-workspace')?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <section
      id="hero-section"
      className="pt-24 sm:pt-32 md:pt-36 pb-12 w-full flex flex-col items-center justify-center text-center overflow-hidden"
    >
      <div className="max-w-4xl mx-auto px-6 sm:px-8 flex flex-col items-center">
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-[#E5DDD3] text-[#111111] text-xs font-semibold tracking-wide uppercase mb-6">
          <FileText className="w-3.5 h-3.5 text-[#111111]" /> Document Restyler Engine
        </div>

        <h1
          id="hero-title"
          className="tracking-tight text-center flex flex-col items-center justify-center"
        >
          <span className="font-display-serif italic font-normal text-4xl sm:text-5xl md:text-6xl lg:text-[64px] xl:text-[72px] text-[#111111] leading-[1.1]">
            Automated Design Transfer,
          </span>
          <span className="font-sans-clean font-extrabold text-4xl sm:text-5xl md:text-6xl lg:text-[64px] xl:text-[72px] text-[#111111] leading-[1.1] mt-1">
            DocStyle Engine for Teams
          </span>
        </h1>

        <p
          id="hero-subtitle"
          className="text-stone-600 text-sm sm:text-base md:text-[17px] font-normal leading-relaxed mt-5 max-w-2xl"
        >
          Extract visual design parameters from reference templates and apply them onto raw text documents with <strong>100% verbatim accuracy</strong>.
        </p>

        <div className="mt-8">
          <button
            id="btn-hero-cta"
            onClick={scrollToWorkspace}
            className="bg-[#111111] hover:bg-black text-white px-8 py-3.5 rounded-full text-sm font-semibold inline-flex items-center gap-2.5 transition-all duration-200 hover:scale-105 active:scale-95 shadow-md cursor-pointer"
          >
            <Play className="w-4 h-4 fill-white" />
            <span>Open Document Restyler</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      </div>

      <div className="w-full mt-12 sm:mt-16 md:mt-20">
        <TeamGallery />
      </div>

      <HeroFeatures />
    </section>
  );
};
