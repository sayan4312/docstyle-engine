import React from 'react';
import { ArrowUpRight, Palette, FileText, CheckCircle2, FileCheck } from 'lucide-react';

interface FeatureGridProps {
  onSelectFeature?: (featureName: string) => void;
}

export const FeatureGrid: React.FC<FeatureGridProps> = ({ onSelectFeature }) => {
  return (
    <section
      id="features"
      className="py-16 sm:py-24 md:py-28 w-full max-w-7xl mx-auto px-6 sm:px-8 lg:px-12"
    >
      {/* Section Header */}
      <div className="text-center max-w-3xl mx-auto mb-16">
        <span className="inline-block px-3.5 py-1 rounded-full bg-[#E5DDD3] text-[#111111] text-xs font-semibold uppercase tracking-wider mb-4 border border-[#d8cec2]">
          Engine Architecture
        </span>
        <h2 className="text-3xl sm:text-4xl md:text-5xl font-serif font-normal text-[#111111] tracking-tight mb-4">
          Engine Capabilities & Infrastructure
        </h2>
        <p className="text-stone-600 font-sans-clean text-sm sm:text-base leading-relaxed">
          Dynamic layout analysis, semantic block classification, and verbatim content preservation.
        </p>
      </div>

      {/* 4 Feature Cards Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 sm:gap-8">
        
        {/* CARD 1: Visual Design Transfer (7 cols) */}
        <div
          id="card-design-transfer"
          onClick={() => onSelectFeature?.('Visual Design Transfer')}
          className="lg:col-span-7 h-[320px] sm:h-[360px] rounded-[30px] overflow-hidden relative group cursor-pointer shadow-md hover:shadow-2xl transition-all duration-500 border border-stone-200/50 bg-[#111111] transform hover:-translate-y-2"
        >
          <img
            src="/artifacts/card_design_transfer_1787650424155.jpg"
            alt="Visual Design Transfer Engine"
            className="w-full h-full object-cover object-center filter brightness-[0.85] group-hover:brightness-100 group-hover:scale-105 transition-all duration-700"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-black/90 via-black/40 to-transparent" />

          <div className="absolute top-6 left-6 right-6 flex items-center justify-between z-10">
            <div className="w-10 h-10 rounded-2xl bg-white/20 backdrop-blur-md flex items-center justify-center text-white border border-white/30">
              <Palette className="w-5 h-5" />
            </div>
            <div className="w-9 h-9 rounded-full bg-white/20 backdrop-blur-md flex items-center justify-center text-white opacity-0 group-hover:opacity-100 transition-opacity">
              <ArrowUpRight className="w-4 h-4" />
            </div>
          </div>

          <div className="absolute bottom-0 left-0 right-0 p-8 text-left z-10">
            <h3 className="text-white font-sans-clean font-extrabold text-2xl sm:text-3xl tracking-tight mb-2">
              Visual Design Transfer
            </h3>
            <p className="text-stone-200 text-sm leading-relaxed max-w-lg">
              Extracts primary accent colors, font families, page margins, line spacing, and table header fill colors directly from template documents.
            </p>
          </div>
        </div>

        {/* CARD 2: Semantic Block Parsing (5 cols) */}
        <div
          id="card-semantic-parsing"
          onClick={() => onSelectFeature?.('Semantic Block Parsing')}
          className="lg:col-span-5 h-[320px] sm:h-[360px] rounded-[30px] overflow-hidden relative group cursor-pointer shadow-md hover:shadow-2xl transition-all duration-500 border border-stone-200/50 bg-[#EDE5DD] transform hover:-translate-y-2"
        >
          <img
            src="/artifacts/card_semantic_parsing_1787650445462.jpg"
            alt="Semantic Block Parsing"
            className="w-full h-full object-cover object-center filter brightness-[0.85] group-hover:brightness-100 group-hover:scale-105 transition-all duration-700"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-black/90 via-black/40 to-transparent" />

          <div className="absolute top-6 left-6 right-6 flex items-center justify-between z-10">
            <div className="w-10 h-10 rounded-2xl bg-white/20 backdrop-blur-md flex items-center justify-center text-white border border-white/30">
              <FileText className="w-5 h-5" />
            </div>
            <div className="w-9 h-9 rounded-full bg-white/20 backdrop-blur-md flex items-center justify-center text-white opacity-0 group-hover:opacity-100 transition-opacity">
              <ArrowUpRight className="w-4 h-4" />
            </div>
          </div>

          <div className="absolute bottom-0 left-0 right-0 p-8 text-left z-10">
            <h3 className="text-white font-sans-clean font-extrabold text-2xl sm:text-3xl tracking-tight mb-2">
              Semantic Parsing
            </h3>
            <p className="text-stone-200 text-sm leading-relaxed">
              Intelligently classifies text into titles, headings, subheadings, body paragraphs, bullet lists, and formatted data tables.
            </p>
          </div>
        </div>

        {/* CARD 3: 100% Verbatim Integrity (5 cols) */}
        <div
          id="card-verbatim-integrity"
          onClick={() => onSelectFeature?.('Verbatim Content Integrity')}
          className="lg:col-span-5 h-[320px] sm:h-[360px] rounded-[30px] overflow-hidden relative group cursor-pointer shadow-md hover:shadow-2xl transition-all duration-500 border border-emerald-900/40 bg-[#2D4A3E] transform hover:-translate-y-2"
        >
          <img
            src="/artifacts/card_verbatim_integrity_1787650610836.jpg"
            alt="Verbatim Content Integrity"
            className="w-full h-full object-cover object-center filter brightness-[0.85] group-hover:brightness-100 group-hover:scale-105 transition-all duration-700"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-black/90 via-black/40 to-transparent" />

          <div className="absolute top-6 left-6 right-6 flex items-center justify-between z-10">
            <div className="w-10 h-10 rounded-2xl bg-white/20 backdrop-blur-md flex items-center justify-center text-white border border-white/30">
              <CheckCircle2 className="w-5 h-5" />
            </div>
            <div className="w-9 h-9 rounded-full bg-white/20 backdrop-blur-md flex items-center justify-center text-white opacity-0 group-hover:opacity-100 transition-opacity">
              <ArrowUpRight className="w-4 h-4" />
            </div>
          </div>

          <div className="absolute bottom-0 left-0 right-0 p-8 text-left z-10">
            <h3 className="text-white font-sans-clean font-extrabold text-2xl sm:text-3xl tracking-tight mb-2">
              100% Verbatim Integrity
            </h3>
            <p className="text-stone-200 text-sm leading-relaxed">
              Automated string similarity validation ensures 100% of input text is preserved without data loss or content alteration.
            </p>
          </div>
        </div>

        {/* CARD 4: Multi-Format Vector Export (7 cols) */}
        <div
          id="card-vector-export"
          onClick={() => onSelectFeature?.('Vector PDF & DOCX Export')}
          className="lg:col-span-7 h-[320px] sm:h-[360px] rounded-[30px] overflow-hidden relative group cursor-pointer shadow-md hover:shadow-2xl transition-all duration-500 border border-amber-900/40 bg-[#3D332A] transform hover:-translate-y-2"
        >
          <img
            src="/artifacts/card_vector_export_1787650668203.jpg"
            alt="DOCX & Vector PDF Export"
            className="w-full h-full object-cover object-center filter brightness-[0.85] group-hover:brightness-100 group-hover:scale-105 transition-all duration-700"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-black/90 via-black/40 to-transparent" />

          <div className="absolute top-6 left-6 right-6 flex items-center justify-between z-10">
            <div className="w-10 h-10 rounded-2xl bg-white/20 backdrop-blur-md flex items-center justify-center text-white border border-white/30">
              <FileCheck className="w-5 h-5" />
            </div>
            <div className="w-9 h-9 rounded-full bg-white/20 backdrop-blur-md flex items-center justify-center text-white opacity-0 group-hover:opacity-100 transition-opacity">
              <ArrowUpRight className="w-4 h-4" />
            </div>
          </div>

          <div className="absolute bottom-0 left-0 right-0 p-8 text-left z-10">
            <h3 className="text-white font-sans-clean font-extrabold text-2xl sm:text-3xl tracking-tight mb-2">
              DOCX & Vector PDF Export
            </h3>
            <p className="text-stone-200 text-sm leading-relaxed max-w-lg">
              Generates styled Microsoft Word documents (.docx) and high-resolution vector PDFs with live browser viewer embedding.
            </p>
          </div>
        </div>

      </div>
    </section>
  );
};
