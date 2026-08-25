export interface PipelineModule {
  id: string;
  number: string;
  name: string;
  title: string;
  role: string;
  description: string;
  imageUrl: string;
  rotation: number;
  translateZ: number;
  translateY: number;
}

export interface ArchitectureFeature {
  number: string;
  title: string;
  description: string;
}

export interface HeroFeature {
  id: string;
  title: string;
  subtitle: string;
  description: string;
  iconName: string;
}

export interface ImpactMetric {
  value: string;
  label: string;
  description: string;
}

export const PIPELINE_MODULES: PipelineModule[] = [
  {
    id: 'style-extractor',
    number: '01',
    name: 'Style Extractor',
    title: 'Style Extractor',
    role: 'OpenXML & PyMuPDF Parser',
    description: 'Dynamically extracts primary/secondary colors, font families, table header fills, and page margins from DOCX and PDF templates.',
    imageUrl: '/assets/card_design_transfer.jpg',
    rotation: -16,
    translateZ: -45,
    translateY: 14
  },
  {
    id: 'canonical-ast',
    number: '02',
    name: 'Canonical AST',
    title: 'Canonical AST',
    role: 'Intermediate Representation',
    description: 'Decouples text content from visual styling using a structured Canonical Intermediate Representation.',
    imageUrl: '/assets/card_semantic_parsing.jpg',
    rotation: -8,
    translateZ: -15,
    translateY: 4
  },
  {
    id: 'classifier-waterfall',
    number: '03',
    name: '5-Layer Classifier',
    title: '5-Layer Classifier',
    role: '5-Layer Semantic Engine',
    description: 'Human-like semantic classification combining OpenXML tags, pattern regex, typography ratios, context windows, and LLM fallback.',
    imageUrl: '/assets/card_classifier.jpg',
    rotation: 0,
    translateZ: 30,
    translateY: -10
  },
  {
    id: 'verbatim-engine',
    number: '04',
    name: 'Verbatim Verifier',
    title: 'Verbatim Verifier',
    role: '100% Integrity Engine',
    description: 'Asserts 100% content preservation with zero text drift, zero summaries, and zero hallucinations.',
    imageUrl: '/assets/card_verbatim_integrity.jpg',
    rotation: 8,
    translateZ: -15,
    translateY: 4
  },
  {
    id: 'pdf-exporter',
    number: '05',
    name: 'PDF Exporter',
    title: 'PDF Exporter',
    role: 'Vector Layout Renderer',
    description: 'Converts restyled Word documents into high-resolution, print-ready vector PDF files with live browser viewing.',
    imageUrl: '/assets/card_vector_export.jpg',
    rotation: 16,
    translateZ: -45,
    translateY: 14
  }
];

export const HERO_FEATURES: HeroFeature[] = [
  {
    id: 'style-dna',
    title: 'Style DNA Extractor',
    subtitle: 'Dynamic OpenXML & Vector Extraction',
    description: 'Reads primary accent colors, font families, table header fills, and margin geometry from reference templates.',
    iconName: 'Palette'
  },
  {
    id: 'semantic-ast',
    title: 'Canonical Document AST',
    subtitle: 'Decoupled Intermediate Representation',
    description: 'Separates content text from visual presentation for clean multi-format document transformation.',
    iconName: 'FileText'
  },
  {
    id: 'verbatim-engine',
    title: 'Verbatim Integrity Engine',
    subtitle: '100% Text Preservation Guarantee',
    description: 'Ensures zero words are lost, omitted, summarized, or hallucinated during automated document restyling.',
    iconName: 'ShieldCheck'
  }
];

export const IMPACT_METRICS: ImpactMetric[] = [
  {
    value: '100%',
    label: 'Verbatim Content Integrity',
    description: 'Zero text modification guarantee'
  },
  {
    value: '5-Layer',
    label: 'Classification Waterfall',
    description: 'OpenXML, Regex, Typography, Context & LLM'
  },
  {
    value: '< 3.5s',
    label: 'Transformation Pipeline Speed',
    description: 'Instant DOCX & Vector PDF Generation'
  }
];

export const ARCHITECTURE_FEATURES: ArchitectureFeature[] = [
  {
    number: '01',
    title: 'Style Token Extraction',
    description: 'Automatically extracts primary/secondary accent colors, typography font families, page margins, and table header fills from reference templates.'
  },
  {
    number: '02',
    title: 'Canonical Document AST',
    description: 'Decouples document content from visual styling using a structured Intermediate Representation (AST) for human-like semantic reasoning.'
  },
  {
    number: '03',
    title: '5-Layer Classification Waterfall',
    description: 'Multi-signal semantic classifier evaluating OpenXML tags, pattern regex, typography size ratios, context windows, and LLM fallback.'
  },
  {
    number: '04',
    title: 'Verbatim Integrity Engine',
    description: 'Guarantees 100% content preservation - zero text lost, modified, or omitted during automated document restyling.'
  }
];
