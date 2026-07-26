import React from "react";
import {
  AbsoluteFill,
  interpolate,
  useCurrentFrame,
  useVideoConfig,
  Easing,
} from "remotion";
import { ScooterIcon } from "./icons";
import { TheBoldFont } from "../load-font";

const ACCENT = "#0074e8";

const Mountain: React.FC<{
  left: string;
  width: number;
  height: number;
  color: string;
  snowColor: string;
}> = ({ left, width, height, color, snowColor }) => (
  <div
    style={{
      position: "absolute",
      left,
      bottom: 0,
      width: 0,
      height: 0,
      borderLeft: `${width / 2}px solid transparent`,
      borderRight: `${width / 2}px solid transparent`,
      borderBottom: `${height}px solid ${color}`,
    }}
  >
    <div
      style={{
        position: "absolute",
        top: 0,
        left: -width * 0.16,
        width: 0,
        height: 0,
        borderLeft: `${width * 0.16}px solid transparent`,
        borderRight: `${width * 0.16}px solid transparent`,
        borderTop: `${height * 0.22}px solid ${snowColor}`,
      }}
    />
  </div>
);

export const Scene2Scooter: React.FC<{ vertical: boolean }> = ({ vertical }) => {
  const frame = useCurrentFrame();
  const { width, height } = useVideoConfig();

  const glideProgress = interpolate(frame, [0, 70], [-0.2, 1.1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.cubic),
  });
  const bob = Math.sin(frame / 5) * 6;

  const scooterSize = Math.min(width, height) * 0.3;
  const scooterX = width * glideProgress;
  const scooterY = height * (vertical ? 0.58 : 0.6) + bob;

  const titleOpacity = interpolate(frame, [6, 18], [0, 1], { extrapolateRight: "clamp" });
  const titleY = interpolate(frame, [6, 18], [24, 0], { extrapolateRight: "clamp" });
  const subOpacity = interpolate(frame, [18, 30], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const titleSize = vertical ? width * 0.1 : height * 0.1;
  const subSize = vertical ? width * 0.04 : height * 0.042;

  return (
    <AbsoluteFill
      style={{
        background: "linear-gradient(180deg, #cfeaff 0%, #eaf6ff 55%, #ffffff 100%)",
      }}
    >
      <Mountain left="4%" width={width * 0.38} height={height * 0.42} color="#8fb3cf" snowColor="#ffffff" />
      <Mountain left="34%" width={width * 0.46} height={height * 0.52} color="#7aa3c4" snowColor="#ffffff" />
      <Mountain left="66%" width={width * 0.4} height={height * 0.38} color="#9dbfda" snowColor="#ffffff" />

      <div
        style={{
          position: "absolute",
          bottom: 0,
          width: "100%",
          height: height * 0.22,
          background: "#dfeeff",
        }}
      />
      {/* road */}
      <div
        style={{
          position: "absolute",
          bottom: 0,
          width: "100%",
          height: height * 0.1,
          background: "#3a4550",
        }}
      />
      <div
        style={{
          position: "absolute",
          bottom: height * 0.048,
          width: "100%",
          height: 4,
          background: "repeating-linear-gradient(90deg, #fff 0 40px, transparent 40px 80px)",
          opacity: 0.7,
        }}
      />

      <div
        style={{
          position: "absolute",
          left: scooterX - scooterSize / 2,
          top: scooterY - scooterSize,
          filter: "drop-shadow(0 12px 14px rgba(20,40,60,0.25))",
        }}
      >
        <ScooterIcon color="#173a5e" size={scooterSize} />
      </div>

      <AbsoluteFill
        style={{
          justifyContent: "flex-start",
          alignItems: "center",
          flexDirection: "column",
          paddingTop: vertical ? height * 0.08 : height * 0.1,
        }}
      >
        <div
          style={{
            fontFamily: TheBoldFont,
            fontSize: titleSize,
            color: "#0e2a44",
            letterSpacing: 2,
            opacity: titleOpacity,
            transform: `translateY(${titleY}px)`,
            textAlign: "center",
          }}
        >
          E-SCOOTER URBANA
        </div>
        <div
          style={{
            fontFamily: "system-ui, sans-serif",
            fontWeight: 600,
            fontSize: subSize,
            color: ACCENT,
            opacity: subOpacity,
            marginTop: 10,
            letterSpacing: 1,
            textAlign: "center",
          }}
        >
          HECHA PARA LAS CALLES DE SUIZA
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
