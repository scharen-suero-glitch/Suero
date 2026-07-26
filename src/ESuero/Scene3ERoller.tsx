import React from "react";
import {
  AbsoluteFill,
  interpolate,
  useCurrentFrame,
  useVideoConfig,
  Easing,
} from "remotion";
import { RollerIcon } from "./icons";
import { GridLines } from "./effects";
import { TheBoldFont } from "../load-font";

const ACCENT = "#2de6c9";

export const Scene3ERoller: React.FC<{ vertical: boolean }> = ({ vertical }) => {
  const frame = useCurrentFrame();
  const { width, height } = useVideoConfig();

  const enter = interpolate(frame, [0, 26], [1.15, 1], {
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.back(1.4)),
  });
  const enterOpacity = interpolate(frame, [0, 14], [0, 1], { extrapolateRight: "clamp" });
  const bob = Math.sin(frame / 6) * 5;

  const rollerSize = Math.min(width, height) * 0.34;

  const titleOpacity = interpolate(frame, [8, 20], [0, 1], { extrapolateRight: "clamp" });
  const titleScale = interpolate(frame, [8, 20], [0.8, 1], { extrapolateRight: "clamp" });
  const subOpacity = interpolate(frame, [20, 32], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const titleSize = vertical ? width * 0.13 : height * 0.13;
  const subSize = vertical ? width * 0.04 : height * 0.042;

  return (
    <AbsoluteFill
      style={{
        background: "linear-gradient(160deg, #0a1620 0%, #0f2430 45%, #123640 100%)",
      }}
    >
      <GridLines color={ACCENT} />

      <AbsoluteFill
        style={{
          justifyContent: "center",
          alignItems: "center",
          flexDirection: "column",
        }}
      >
        <div
          style={{
            fontFamily: TheBoldFont,
            fontSize: titleSize,
            color: "#f2fffb",
            letterSpacing: 3,
            opacity: titleOpacity,
            transform: `scale(${titleScale})`,
            textShadow: `0 0 30px ${ACCENT}66`,
          }}
        >
          E-ROLLER
        </div>

        <div
          style={{
            transform: `scale(${enter}) translateY(${bob}px)`,
            opacity: enterOpacity,
            margin: "18px 0",
            filter: `drop-shadow(0 0 26px ${ACCENT}55)`,
          }}
        >
          <RollerIcon color={ACCENT} size={rollerSize} />
        </div>

        <div
          style={{
            fontFamily: "system-ui, sans-serif",
            fontWeight: 600,
            fontSize: subSize,
            color: "#bfeee6",
            opacity: subOpacity,
            letterSpacing: 1,
            textAlign: "center",
          }}
        >
          TU CIUDAD, TU RITMO
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
