import React from 'react';
import { ArrowRight, CheckCircle2, FileCheck, FileText, Palette } from 'lucide-react';
import { IMPACT_METRICS } from '../data/projectData';

export const ImpactShowcase: React.FC = () => {
  const scrollToWorkspace = () => {
    document.getElementById('docstyle-workspace')?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <section
      id="impact"
      className="py-16 sm:py-24 md:py-28 w-full max-w-7xl mx-auto px-6 sm:px-8 lg:px-12"
    >
      <div className="text-center max-w-3xl mx-auto mb-12 sm:mb-16">
        <span className="text-xs font-semibold uppercase tracking-wider text-stone-500 bg-[#E5DDD3] px-3.5 py-1.5 rounded-full">
          Engine Performance
        </span>
        <h2 className="text-3xl sm:text-4xl md:text-5xl font-bold text-[#111111] tracking-tight font-sans-clean leading-[1.15] mt-4">
          Proven Accuracy, Real Impact
        </h2>
        <p className="text-stone-600 text-sm sm:text-base leading-relaxed mt-3 max-w-xl mx-auto">
          Built for teams that demand flawless design transfer without risking text loss or manual reformatting errors.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 sm:gap-8 mb-16">
        <div className="bg-[#EFE8DF] rounded-[28px] p-6 sm:p-8 flex flex-col justify-between min-h-[340px] border border-stone-200/60 shadow-xs hover:shadow-md transition-all">
          <div>
            <div className="w-10 h-10 rounded-2xl bg-white text-[#111111] flex items-center justify-center mb-4 shadow-xs">
              <Palette className="w-5 h-5" />
            </div>
            <span className="text-[11px] font-semibold uppercase tracking-wider text-stone-500">
              Style DNA Extractor
            </span>
            <h4 className="text-xl font-bold text-[#111111] mt-1">
              Automated Style Extraction
            </h4>
            <p className="text-xs text-stone-600 mt-2 leading-relaxed">
              Inspects reference XML structures to pull exact primary colors, typography families, line spacing, margins, and table header fills.
            </p>
          </div>
          <div className="pt-4 border-t border-stone-300/60 text-xs font-bold text-[#111111] flex items-center gap-1.5">
            <CheckCircle2 className="w-4 h-4 text-emerald-600" /> Extracts 10+ Design Tokens
          </div>
        </div>

        <div className="bg-[#EAE2D8] rounded-[28px] p-6 sm:p-8 flex flex-col justify-between min-h-[340px] border border-stone-200/60 shadow-xs hover:shadow-md transition-all">
          <div>
            <div className="w-10 h-10 rounded-2xl bg-white text-emerald-700 flex items-center justify-center mb-4 shadow-xs">
              <CheckCircle2 className="w-5 h-5" />
            </div>
            <span className="text-[11px] font-semibold uppercase tracking-wider text-stone-500">
              Verbatim Integrity
            </span>
            <h4 className="text-xl font-bold text-[#111111] mt-1">
              100% Content Preservation
            </h4>
            <p className="text-xs text-stone-600 mt-2 leading-relaxed">
              Automated string similarity verification validates every line of source text against output documents to guarantee zero data loss.
            </p>
          </div>
          <div className="pt-4 border-t border-stone-300/60 text-xs font-bold text-emerald-700 flex items-center gap-1.5">
            <FileCheck className="w-4 h-4 text-emerald-600" /> 100% Verbatim Accuracy
          </div>
        </div>

        <div className="bg-[#BCA998] rounded-[28px] p-6 sm:p-8 flex flex-col justify-between min-h-[340px] text-white shadow-xs hover:shadow-md transition-all">
          <div>
            <div className="w-10 h-10 rounded-2xl bg-white/20 text-white flex items-center justify-center mb-4">
              <FileCheck className="w-5 h-5" />
            </div>
            <span className="text-[11px] font-semibold uppercase tracking-wider text-white/80">
              Vector PDF Export
            </span>
            <h4 className="text-xl font-bold text-white mt-1">
              Print-Ready Vector Output
            </h4>
            <p className="text-xs text-white/90 mt-2 leading-relaxed">
              Generates Word documents (.docx) and high-resolution vector PDFs simultaneously with live embedded browser viewing.
            </p>
          </div>
          <div className="pt-4 border-t border-white/20 text-xs font-bold text-white flex items-center gap-1.5">
            <FileText className="w-4 h-4 text-stone-200" /> Multi-Format Support
          </div>
        </div>
      </div>

      <div className="bg-[#EDE5DD]/60 rounded-[32px] p-8 sm:p-12 border border-stone-200/60">
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-6 sm:gap-8">
          {IMPACT_METRICS.map((metric, idx) => (
            <div key={idx} className="text-center sm:text-left">
              <p className="text-3xl sm:text-4xl md:text-5xl font-extrabold text-[#111111] tracking-tight font-sans-clean">
                {metric.value}
              </p>
              <p className="text-sm font-bold text-stone-800 mt-1.5">
                {metric.label}
              </p>
              <p className="text-xs text-stone-500 mt-1 leading-relaxed max-w-[200px] mx-auto sm:mx-0">
                {metric.description}
              </p>
            </div>
          ))}
        </div>
      </div>

      <div className="mt-16 sm:mt-24 text-center bg-[#111111] text-white rounded-[32px] p-8 sm:p-14 lg:p-16 relative overflow-hidden">
        <div className="max-w-2xl mx-auto relative z-10">
          <h3 className="font-display-serif italic text-3xl sm:text-4xl md:text-5xl font-normal">
            Ready to restyle your documents?
          </h3>
          <p className="font-sans-clean font-bold text-2xl sm:text-3xl mt-1 text-white/90">
            Start using DocStyle Engine today.
          </p>
          <p className="text-xs sm:text-sm text-stone-400 mt-3 max-w-md mx-auto">
            Upload your reference design document and raw text to generate styled Word documents and vector PDFs instantly.
          </p>
          <div className="mt-8 flex items-center justify-center">
            <button
              id="btn-bottom-cta"
              onClick={scrollToWorkspace}
              className="bg-white text-black hover:bg-stone-100 px-8 py-3.5 rounded-full text-sm font-semibold transition-all transform hover:scale-105 active:scale-95 flex items-center justify-center gap-2 cursor-pointer shadow-lg"
            >
              <FileText className="w-4 h-4 text-[#111111]" />
              <span>Start Restyling Now</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    </section>
  );
};
