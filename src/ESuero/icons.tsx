import React from "react";

type IconProps = {
  color: string;
  size: number;
};

// Stylised dirt bike silhouette (Sur-Ron style): knobby wheels, long-travel
// forks, crouched rider — built from primitives, not a traced photo.
export const MotoIcon: React.FC<IconProps> = ({ color, size }) => (
  <svg
    width={size}
    height={size * 0.72}
    viewBox="0 0 200 144"
    style={{ overflow: "visible" }}
  >
    <g fill="none" stroke={color} strokeWidth={7} strokeLinecap="round" strokeLinejoin="round">
      {/* wheels */}
      <circle cx={40} cy={112} r={26} fill="none" />
      <circle cx={160} cy={112} r={26} fill="none" />
      <circle cx={40} cy={112} r={9} fill={color} stroke="none" />
      <circle cx={160} cy={112} r={9} fill={color} stroke="none" />
      {/* rear suspension + frame */}
      <path d="M40 112 L92 70 L120 70 L160 112" />
      <path d="M92 70 L100 40" />
      {/* front fork (long travel, dirt-bike style) */}
      <path d="M160 112 L128 46" />
      <path d="M128 46 L142 34" />
      {/* handlebar */}
      <path d="M100 40 L118 32" />
      {/* seat + tank */}
      <path d="M92 70 L60 78 L46 74" fill={color} stroke="none" opacity={0.9} />
      {/* rider, crouched attack position */}
      <path
        d="M78 70 C70 52 74 34 92 24 C100 19 112 20 118 26"
        strokeWidth={9}
      />
      <circle cx={122} cy={20} r={11} fill={color} stroke="none" />
    </g>
  </svg>
);

// Stand-up e-scooter with rider, upright commuter posture.
export const ScooterIcon: React.FC<IconProps> = ({ color, size }) => (
  <svg
    width={size}
    height={size * 1.14}
    viewBox="0 0 140 160"
    style={{ overflow: "visible" }}
  >
    <g fill="none" stroke={color} strokeWidth={6} strokeLinecap="round" strokeLinejoin="round">
      {/* wheels */}
      <circle cx={26} cy={136} r={14} />
      <circle cx={100} cy={136} r={14} />
      <circle cx={26} cy={136} r={4} fill={color} stroke="none" />
      <circle cx={100} cy={136} r={4} fill={color} stroke="none" />
      {/* deck */}
      <path d="M26 124 L100 124" />
      {/* steering column + handlebar */}
      <path d="M100 124 L100 40" />
      <path d="M84 36 L116 36" />
      {/* rider: torso, head, arm to handlebar */}
      <path d="M60 124 L60 54" strokeWidth={9} />
      <circle cx={60} cy={44} r={11} fill={color} stroke="none" />
      <path d="M60 80 L92 40" strokeWidth={8} />
    </g>
  </svg>
);

// Seated e-moped ("Roller"): bigger body, windshield, seated rider.
export const RollerIcon: React.FC<IconProps> = ({ color, size }) => (
  <svg
    width={size}
    height={size * 0.78}
    viewBox="0 0 200 156"
    style={{ overflow: "visible" }}
  >
    <g fill="none" stroke={color} strokeWidth={7} strokeLinecap="round" strokeLinejoin="round">
      <circle cx={44} cy={122} r={24} />
      <circle cx={156} cy={122} r={24} />
      <circle cx={44} cy={122} r={8} fill={color} stroke="none" />
      <circle cx={156} cy={122} r={8} fill={color} stroke="none" />
      {/* body / floorboard */}
      <path
        d="M44 122 L60 100 C70 84 96 78 118 82 L150 90 L156 122"
        fill={color}
        stroke="none"
        opacity={0.9}
      />
      {/* windshield + handlebar */}
      <path d="M118 82 L128 46" />
      <path d="M128 46 L150 40" />
      {/* seat + backrest */}
      <path d="M60 100 L52 84" />
      {/* rider seated */}
      <path d="M100 90 L100 56" strokeWidth={9} />
      <circle cx={100} cy={46} r={11} fill={color} stroke="none" />
      <path d="M100 62 L128 50" strokeWidth={8} />
    </g>
  </svg>
);
