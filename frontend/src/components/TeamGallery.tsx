import React, { useState, useRef, useEffect } from 'react';
import { PIPELINE_MODULES, PipelineModule } from '../data/projectData';
import { Palette, FileCode2, Layers, ShieldCheck, FileCheck, ArrowUpRight, CheckCircle2, FileText } from 'lucide-react';

interface TeamGalleryProps {
  onSelectMember?: (module: PipelineModule) => void;
}

export const TeamGallery: React.FC<TeamGalleryProps> = ({ onSelectMember }) => {
  const [hoveredId, setHoveredId] = useState<string | null>(null);
  const [mouseOffset, setMouseOffset] = useState({ x: 0, y: 0 });
  const [isMobile, setIsMobile] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleResize = () => {
      setIsMobile(window.innerWidth < 640);
    };
    handleResize();
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    if (isMobile || !containerRef.current) return;
    const rect = containerRef.current.getBoundingClientRect();
    const x = ((e.clientX - rect.left) / rect.width - 0.5) * 2;
    const y = ((e.clientY - rect.top) / rect.height - 0.5) * 2;
    setMouseOffset({ x, y });
  };

  const handleMouseLeave = () => {
    setMouseOffset({ x: 0, y: 0 });
    setHoveredId(null);
  };

  return (
    <div
      id="team-gallery-container"
      ref={containerRef}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
      className="w-full relative py-6 sm:py-10 md:py-12 bg-[#F4EFEA] select-none"
    >
      {/* Mobile Swipe Indicator */}
      <div className="flex sm:hidden items-center justify-center gap-1.5 text-xs text-stone-500 font-semibold mb-2">
        <span>← Swipe to explore pipeline cards →</span>
      </div>

      {/* Track with Horizontal Scroll (Flat on Mobile, 3D Arch Stage on Desktop) */}
      <div className="w-full overflow-x-auto no-scrollbar py-2 sm:py-6 scroll-smooth cursor-grab active:cursor-grabbing px-4 sm:px-0">
        {/* Stage Container */}
        <div
          className={`${
            isMobile
              ? 'flex items-center gap-3.5 px-4 snap-x snap-mandatory justify-start'
              : 'perspective-stage w-full max-w-[1450px] mx-auto flex items-center justify-center min-h-[500px] sm:min-h-[540px] md:min-h-[580px] px-4 sm:px-8'
          }`}
        >
          <div
            className={`${
              isMobile
                ? 'flex items-center gap-3.5'
                : 'preserve-3d flex items-center justify-center -space-x-1 sm:space-x-2 md:space-x-4 lg:space-x-6'
            } transition-transform duration-300 ease-out`}
            style={
              isMobile
                ? undefined
                : {
                    transform: `rotateY(${mouseOffset.x * 4}deg) rotateX(${-mouseOffset.y * 2}deg)`,
                  }
            }
          >
            {PIPELINE_MODULES.map((module, index) => {
              const isHovered = hoveredId === module.id;

              // Curved DOWN Arch offsets for desktop
              const baseRotations = [-22, -11, 0, 11, 22];
              const baseTranslateZ = [-40, 0, 40, 0, -40];
              const baseTranslateY = [24, 5, -24, 5, 24];

              const rot = isHovered ? 0 : baseRotations[index] + mouseOffset.x * 3;
              const tz = isHovered ? 80 : baseTranslateZ[index];
              const ty = isHovered ? baseTranslateY[index] - 22 : baseTranslateY[index];
              const sc = isHovered ? 1.08 : 1.0;
              const zIdx = isHovered ? 50 : (30 - Math.abs(index - 2) * 5);

              return (
                <div
                  key={module.id}
                  id={`pipeline-card-${module.id}`}
                  onClick={() => onSelectMember?.(module)}
                  onMouseEnter={() => setHoveredId(module.id)}
                  className={`relative cursor-pointer transition-all duration-300 ease-out group shrink-0 ${
                    isMobile ? 'snap-center' : ''
                  }`}
                  style={
                    isMobile
                      ? { transform: isHovered ? 'scale(1.02)' : 'none', zIndex: 10 }
                      : {
                          transform: `translate3d(0px, ${ty}px, ${tz}px) rotateY(${rot}deg) scale(${sc})`,
                          transformOrigin: 'center center',
                          zIndex: zIdx,
                        }
                  }
                >
                  {/* Clean Flat Responsive Card for Mobile / 3D Card for Desktop */}
                  <div
                    className="w-[230px] h-[360px] xs:w-[250px] xs:h-[380px] sm:w-[220px] sm:h-[370px] md:w-[245px] md:h-[410px] lg:w-[265px] lg:h-[440px] rounded-[32px] sm:rounded-[44px] overflow-hidden shadow-xl group-hover:shadow-[0_25px_60px_rgba(0,0,0,0.35)] transition-all duration-500 relative bg-[#111111] border border-stone-800/90 group-hover:border-[#E5DDD3]/50 flex flex-col justify-between p-4 sm:p-6"
                  >
                    {/* Subtle Radial Warm Glow on Hover */}
                    <div className="absolute inset-0 bg-gradient-to-br from-white/5 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none" />

                    {/* Top Bar: Website Neutral Cream Badge & Action Arrow */}
                    <div className="relative z-10 flex items-center justify-between">
                      <div className="w-8 h-8 sm:w-9 sm:h-9 rounded-full bg-[#E5DDD3] text-[#111111] border border-[#D8CEC2] flex items-center justify-center text-xs font-extrabold shadow-xs group-hover:scale-105 transition-transform duration-300">
                        {module.number}
                      </div>

                      <div className="w-8 h-8 sm:w-9 sm:h-9 rounded-full bg-stone-800/80 text-stone-300 border border-stone-700 flex items-center justify-center opacity-100 sm:opacity-0 group-hover:opacity-100 group-hover:bg-[#E5DDD3] group-hover:text-[#111111] group-hover:scale-105 transition-all duration-300 shadow-xs">
                        <ArrowUpRight className="w-4 h-4" />
                      </div>
                    </div>

                    {/* Website Design Diagram Center Area */}
                    <div className="relative z-10 my-auto py-2 flex flex-col items-center justify-center w-full">
                      {index === 0 && (
                        /* Card 01: Style Extractor - Website Theme Color Tokens */
                        <div className="w-full bg-[#1A1A1D] border border-stone-800 group-hover:border-stone-700 transition-colors duration-300 rounded-2xl p-3 sm:p-4 text-left">
                          <div className="flex items-center justify-between mb-2">
                            <span className="text-[10px] font-bold text-[#E5DDD3] uppercase tracking-wider flex items-center gap-1">
                              <Palette className="w-3 h-3 text-[#E5DDD3]" /> Style Tokens
                            </span>
                            <span className="text-[9px] text-stone-400 font-mono">DOCX</span>
                          </div>
                          {/* Color Swatches matching website palette */}
                          <div className="flex items-center gap-2 mb-3">
                            <div className="w-6 h-6 rounded-full bg-[#111111] ring-1 ring-stone-700 shadow-xs" title="#111111" />
                            <div className="w-6 h-6 rounded-full bg-[#E5DDD3] ring-1 ring-stone-500 shadow-xs" title="#E5DDD3" />
                            <div className="w-6 h-6 rounded-full bg-[#F4EFEA] ring-1 ring-stone-400 shadow-xs" title="#F4EFEA" />
                            <div className="w-6 h-6 rounded-full bg-[#3D332A] ring-1 ring-stone-700 shadow-xs" title="#3D332A" />
                          </div>
                          <div className="pt-2 border-t border-stone-800 flex items-center justify-between">
                            <span className="font-serif italic text-stone-200 text-xs sm:text-sm font-semibold">Instrument Serif</span>
                            <span className="text-[9px] text-stone-400 font-mono">Primary</span>
                          </div>
                        </div>
                      )}

                      {index === 1 && (
                        /* Card 02: Canonical AST - Neutral Code Tree */
                        <div className="w-full bg-[#1A1A1D] border border-stone-800 group-hover:border-stone-700 transition-colors duration-300 rounded-2xl p-3 sm:p-4 text-left">
                          <div className="flex items-center justify-between mb-2">
                            <span className="text-[10px] font-bold text-[#E5DDD3] uppercase tracking-wider flex items-center gap-1">
                              <FileCode2 className="w-3 h-3 text-[#E5DDD3]" /> Canonical AST
                            </span>
                            <span className="text-[9px] text-stone-400 font-mono">IR</span>
                          </div>
                          <div className="space-y-1.5 font-mono text-[10px]">
                            <div className="bg-stone-900 border border-stone-700 text-stone-200 px-2 py-1 rounded-md font-bold flex items-center justify-between">
                              <span>&lt;DocumentAST&gt;</span>
                              <span className="text-[8px] bg-[#E5DDD3] text-[#111111] px-1 rounded font-sans font-bold">root</span>
                            </div>
                            <div className="pl-3 border-l border-stone-700 space-y-1">
                              <div className="bg-stone-900 border border-stone-800 text-stone-300 px-2 py-0.5 rounded text-[9px] flex items-center justify-between">
                                <span>├─ &lt;Heading1&gt;</span>
                                <span className="text-[8px] text-stone-400 font-sans">h1</span>
                              </div>
                              <div className="bg-stone-900 border border-stone-800 text-stone-300 px-2 py-0.5 rounded text-[9px] flex items-center justify-between">
                                <span>└─ &lt;Paragraph&gt;</span>
                                <span className="text-[8px] text-stone-400 font-sans">body</span>
                              </div>
                            </div>
                          </div>
                        </div>
                      )}

                      {index === 2 && (
                        /* Card 03: 5-Layer Classifier - Neutral Waterfall */
                        <div className="w-full bg-[#1A1A1D] border border-stone-800 group-hover:border-stone-700 transition-colors duration-300 rounded-2xl p-2.5 sm:p-3 text-left space-y-1">
                          <div className="flex items-center justify-between mb-1">
                            <span className="text-[10px] font-bold text-[#E5DDD3] uppercase tracking-wider flex items-center gap-1">
                              <Layers className="w-3 h-3 text-[#E5DDD3]" /> 5-Layer Waterfall
                            </span>
                          </div>
                          <div className="bg-stone-900 border border-stone-800 text-stone-200 px-2 py-0.5 rounded text-[9px] font-semibold flex items-center justify-between">
                            <span>01 OpenXML Tag</span>
                            <span className="w-1.5 h-1.5 rounded-full bg-[#E5DDD3]" />
                          </div>
                          <div className="bg-stone-900 border border-stone-800 text-stone-200 px-2 py-0.5 rounded text-[9px] font-semibold flex items-center justify-between">
                            <span>02 Pattern Regex</span>
                            <span className="w-1.5 h-1.5 rounded-full bg-[#E5DDD3]" />
                          </div>
                          <div className="bg-stone-900 border border-stone-800 text-stone-200 px-2 py-0.5 rounded text-[9px] font-semibold flex items-center justify-between">
                            <span>03 Typography Ratio</span>
                            <span className="w-1.5 h-1.5 rounded-full bg-[#E5DDD3]" />
                          </div>
                          <div className="bg-stone-900 border border-stone-800 text-stone-200 px-2 py-0.5 rounded text-[9px] font-semibold flex items-center justify-between">
                            <span>04 Context Window</span>
                            <span className="w-1.5 h-1.5 rounded-full bg-[#E5DDD3]" />
                          </div>
                          <div className="bg-stone-900 border border-stone-800 text-stone-200 px-2 py-0.5 rounded text-[9px] font-semibold flex items-center justify-between">
                            <span>05 LLM Fallback</span>
                            <span className="w-1.5 h-1.5 rounded-full bg-[#E5DDD3]" />
                          </div>
                        </div>
                      )}

                      {index === 3 && (
                        /* Card 04: Verbatim Verifier - Neutral Integrity Audit */
                        <div className="w-full bg-[#1A1A1D] border border-stone-800 group-hover:border-stone-700 transition-colors duration-300 rounded-2xl p-3 sm:p-4 text-left">
                          <div className="flex items-center justify-between mb-2">
                            <span className="text-[10px] font-bold text-[#E5DDD3] uppercase tracking-wider flex items-center gap-1">
                              <ShieldCheck className="w-3.5 h-3.5 text-[#E5DDD3]" /> Verbatim Engine
                            </span>
                            <span className="text-[9px] text-[#E5DDD3] font-mono font-bold">100%</span>
                          </div>
                          <div className="bg-stone-900 border border-stone-800 rounded-xl p-2.5 flex items-center gap-2 mb-2">
                            <CheckCircle2 className="w-5 h-5 text-[#E5DDD3] shrink-0" />
                            <div>
                              <div className="text-white text-xs font-extrabold leading-none">0 Words Lost</div>
                              <div className="text-[9px] text-stone-400 mt-0.5">100% String Preservation</div>
                            </div>
                          </div>
                          <div className="w-full bg-stone-900 h-1.5 rounded-full overflow-hidden">
                            <div className="bg-[#E5DDD3] h-full w-full" />
                          </div>
                        </div>
                      )}

                      {index === 4 && (
                        /* Card 05: PDF Exporter - Neutral Layout Renderer */
                        <div className="w-full bg-[#1A1A1D] border border-stone-800 group-hover:border-stone-700 transition-colors duration-300 rounded-2xl p-3 sm:p-4 text-left">
                          <div className="flex items-center justify-between mb-2">
                            <span className="text-[10px] font-bold text-[#E5DDD3] uppercase tracking-wider flex items-center gap-1">
                              <FileCheck className="w-3.5 h-3.5 text-[#E5DDD3]" /> Vector Exporter
                            </span>
                            <span className="text-[9px] text-stone-400 font-mono">DOCX/PDF</span>
                          </div>
                          <div className="flex items-center justify-between bg-stone-900 border border-stone-800 p-2 rounded-xl mb-2">
                            <div className="flex items-center gap-1.5">
                              <FileText className="w-4 h-4 text-stone-300" />
                              <span className="text-[10px] font-bold text-white">.DOCX</span>
                            </div>
                            <span className="text-[#E5DDD3] text-xs font-bold">➔</span>
                            <div className="flex items-center gap-1.5">
                              <FileCheck className="w-4 h-4 text-[#E5DDD3]" />
                              <span className="text-[10px] font-bold text-white">.PDF</span>
                            </div>
                          </div>
                          <div className="flex items-center justify-between text-[9px] text-stone-400 pt-1 border-t border-stone-800">
                            <span>Print Quality</span>
                            <span className="text-[#E5DDD3] font-bold">Vector PDF</span>
                          </div>
                        </div>
                      )}
                    </div>

                    {/* Bottom Metadata & Title strictly following site typography */}
                    <div className="relative z-10 text-left pt-2 border-t border-stone-800">
                      <span className="inline-block px-2.5 py-0.5 rounded-full text-[9px] sm:text-[10px] font-semibold uppercase tracking-wider mb-1.5 bg-[#E5DDD3] text-[#111111] border border-[#D8CEC2]">
                        {module.role.split(' ')[0]} Engine
                      </span>

                      <h3 className="text-white text-base sm:text-lg font-extrabold truncate leading-tight font-sans-clean tracking-tight">
                        {module.name}
                      </h3>

                      <p className="text-stone-400 text-[10px] sm:text-[11px] leading-snug mt-1 font-normal line-clamp-2">
                        {module.description}
                      </p>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
};
