export interface TeamMember {
  id: string;
  name: string;
  role: string;
  imageUrl: string;
  bgColor: string;
  rotation: number; // degrees for 3D perspective arc
  translateZ: number; // px for 3D depth
  translateY: number; // subtle curve offset
}

export interface FeatureColumn {
  id: string;
  title: string;
  description: string;
}

export interface BentoCard {
  id: string;
  title: string;
  description: string;
  type: 'image-overlay' | 'solid-light' | 'solid-taupe' | 'split-green';
  imageUrl?: string;
  personImageUrl?: string;
  bgColor?: string;
  textColor?: string;
}

export interface MetricItem {
  value: string;
  label: string;
  description: string;
}
