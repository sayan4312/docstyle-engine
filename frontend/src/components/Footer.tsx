import React from 'react';
import { FileText, ArrowUp } from 'lucide-react';

export const Footer: React.FC = () => {
  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const scrollToWorkspace = () => {
    document.getElementById('docstyle-workspace')?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <footer className="w-full border-none bg-[#F4EFEA] py-8 px-6 sm:px-8 lg:px-12">
      <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
        {/* Left: Brand Logo & Copyright */}
        <div className="flex items-center gap-3">
          <FileText className="w-5 h-5 text-[#111111]" />
          <span className="font-extrabold text-sm text-[#111111] font-sans-clean">
            DocStyle Engine
          </span>
          <span className="text-stone-400 text-xs hidden sm:inline">•</span>
          <span className="text-stone-500 text-xs">
            © {new Date().getFullYear()} DocStyle Engine. All rights reserved.
          </span>
        </div>

        {/* Right: Quick Links & Back To Top */}
        <div className="flex items-center gap-6 text-xs text-stone-600 font-medium">
          <button
            onClick={scrollToWorkspace}
            className="hover:text-[#111111] transition-colors cursor-pointer"
          >
            Restyler Workspace
          </button>
          <a
            href="#features"
            className="hover:text-[#111111] transition-colors"
          >
            Features
          </a>
          <button
            onClick={scrollToTop}
            className="w-8 h-8 rounded-full bg-[#E5DDD3] hover:bg-[#111111] hover:text-white text-[#111111] flex items-center justify-center transition-all cursor-pointer shadow-2xs ml-2"
            title="Back to Top"
          >
            <ArrowUp className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>
    </footer>
  );
};
