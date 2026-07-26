import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";

// Deterministic pseudo-random in [0, 1), seeded by an integer so renders are
// reproducible across frames/machines (no Math.random()).
const seeded = (seed: number) => {
  const x = Math.sin(seed * 12.9898) * 43758.5453;
  return x - Math.floor(x);
};

export const DustBurst: React.FC<{
  triggerFrame: number;
  color: string;
  originX: number;
  originY: number;
}> = ({ triggerFrame, color, originX, originY }) => {
  const frame = useCurrentFrame();
  const t = frame - triggerFrame;
  if (t < 0 || t > 40) {
    return null;
  }

  const particles = new Array(14).fill(0).map((_, i) => {
    const angle = seeded(i + 1) * Math.PI - Math.PI / 2 - Math.PI / 6;
    const distance = interpolate(t, [0, 30], [0, 60 + seeded(i + 20) * 90], {
      extrapolateRight: "clamp",
    });
    const x = originX + Math.cos(angle) * distance;
    const y = originY - Math.abs(Math.sin(angle) * distance * 0.6);
    const opacity = interpolate(t, [0, 6, 30], [0, 0.8, 0], {
      extrapolateRight: "clamp",
    });
    const size = 10 + seeded(i + 40) * 22;
    return { x, y, opacity, size, key: i };
  });

  return (
    <>
      {particles.map((p) => (
        <div
          key={p.key}
          style={{
            position: "absolute",
            left: p.x,
            top: p.y,
            width: p.size,
            height: p.size,
            borderRadius: "50%",
            background: color,
            opacity: p.opacity,
            filter: "blur(2px)",
          }}
        />
      ))}
    </>
  );
};

export const SpeedLines: React.FC<{
  color: string;
  intensity?: number;
}> = ({ color, intensity = 1 }) => {
  const frame = useCurrentFrame();
  const lines = new Array(9).fill(0).map((_, i) => {
    const baseY = 10 + i * (100 / 9);
    const speed = 26 + seeded(i + 5) * 18;
    const offset = ((frame * speed) % 160) - 80;
    const length = 90 + seeded(i + 60) * 140;
    return { baseY, offset, length, key: i };
  });

  return (
    <AbsoluteFill style={{ overflow: "hidden" }}>
      {lines.map((l) => (
        <div
          key={l.key}
          style={{
            position: "absolute",
            left: `calc(${l.offset}% )`,
            top: `${l.baseY}%`,
            width: l.length,
            height: 3,
            background: color,
            opacity: 0.18 * intensity,
            transform: "translateX(-50%)",
            borderRadius: 4,
          }}
        />
      ))}
    </AbsoluteFill>
  );
};

export const GridLines: React.FC<{ color: string }> = ({ color }) => {
  const frame = useCurrentFrame();
  const shift = (frame * 2) % 60;
  return (
    <AbsoluteFill
      style={{
        opacity: 0.16,
        backgroundImage: `linear-gradient(${color} 1px, transparent 1px), linear-gradient(90deg, ${color} 1px, transparent 1px)`,
        backgroundSize: "60px 60px",
        backgroundPosition: `0 ${shift}px`,
        transform: "perspective(600px) rotateX(55deg) scale(2)",
        transformOrigin: "50% 100%",
      }}
    />
  );
};
