import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { TheBoldFont } from "../load-font";

const ACCENT = "#c6ff3d";

export const Outro: React.FC<{ vertical: boolean }> = ({ vertical }) => {
  const frame = useCurrentFrame();
  const { width, height } = useVideoConfig();

  const logoScale = interpolate(frame, [0, 14], [0.6, 1], { extrapolateRight: "clamp" });
  const logoOpacity = interpolate(frame, [0, 14], [0, 1], { extrapolateRight: "clamp" });
  const glow = 0.5 + Math.sin(frame / 8) * 0.25;

  const taglineOpacity = interpolate(frame, [16, 26], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const ctaOpacity = interpolate(frame, [26, 36], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const ctaPulse = 1 + Math.sin(frame / 6) * 0.03;

  const logoSize = vertical ? width * 0.14 : height * 0.15;
  const tagSize = vertical ? width * 0.045 : height * 0.05;

  return (
    <AbsoluteFill
      style={{
        background: "#0b0b0d",
        justifyContent: "center",
        alignItems: "center",
        flexDirection: "column",
      }}
    >
      <div
        style={{
          fontFamily: TheBoldFont,
          fontSize: logoSize,
          color: "#ffffff",
          opacity: logoOpacity,
          transform: `scale(${logoScale})`,
          textShadow: `0 0 ${40 * glow}px ${ACCENT}`,
          letterSpacing: 2,
        }}
      >
        E-SUERO
      </div>
      <div
        style={{
          fontFamily: "system-ui, sans-serif",
          fontWeight: 600,
          fontSize: tagSize,
          color: "#d8d8d8",
          opacity: taglineOpacity,
          marginTop: 14,
          textAlign: "center",
        }}
      >
        Movilidad eléctrica para cada terreno
      </div>
      <div
        style={{
          marginTop: 34,
          padding: "16px 40px",
          borderRadius: 999,
          background: ACCENT,
          opacity: ctaOpacity,
          transform: `scale(${ctaPulse})`,
          fontFamily: "system-ui, sans-serif",
          fontWeight: 700,
          fontSize: tagSize * 0.7,
          color: "#0b0b0d",
          letterSpacing: 0.5,
        }}
      >
        DESCÚBRELOS EN E-SUERO
      </div>
    </AbsoluteFill>
  );
};
