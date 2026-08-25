import React from 'react';
import { HERO_FEATURES } from '../data/projectData';

export const HeroFeatures: React.FC = () => {
  return (
    <div
      id="hero-features-container"
      className="w-full max-w-5xl mx-auto px-4 sm:px-6 md:px-8 mt-10 sm:mt-14 lg:mt-16"
    >
      {/* 3 White Feature Cards Grid matching screenshot */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 sm:gap-8">
        {HERO_FEATURES.map((feature, idx) => (
          <div
            key={feature.id}
            id={`hero-feature-item-${idx + 1}`}
            className="flex flex-col items-center text-center p-8 sm:p-9 rounded-[32px] bg-white border border-[#EADBCE] shadow-[0_10px_30px_rgba(0,0,0,0.03)] hover:shadow-[0_20px_45px_rgba(0,0,0,0.08)] hover:-translate-y-1.5 transition-all duration-300 group cursor-default"
          >
            {/* Centered Circular Number Badge */}
            <div className="w-10 h-10 rounded-full bg-[#F5EFE8] border border-[#E8DCCF] flex items-center justify-center text-[#1A1A1A] font-bold text-xs tracking-wider mb-5 shadow-xs group-hover:bg-[#111111] group-hover:text-white transition-colors duration-300">
              0{idx + 1}
            </div>

            {/* Title */}
            <h3 className="text-[#1A1A1A] font-extrabold text-lg sm:text-xl tracking-tight mb-3 font-sans-clean group-hover:text-black">
              {feature.title}
            </h3>

            {/* Description */}
            <p className="text-stone-500 text-xs sm:text-sm leading-relaxed font-normal max-w-[290px]">
              {feature.description}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
};
