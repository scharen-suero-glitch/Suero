import React from "react";
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
  Easing,
} from "remotion";
import { MotoIcon } from "./icons";
import { DustBurst, SpeedLines } from "./effects";
import { TheBoldFont } from "../load-font";

const ACCENT = "#c6ff3d";

export const Scene1SurRon: React.FC<{ vertical: boolean }> = ({ vertical }) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();

  const landingFrame = 55;

  // Phase 1: parabolic jump arc, enters low-left, peaks mid-air, lands
  // on-screen at ~75% width so the impact (and dust) is actually visible.
  // Phase 2: bike rides off-screen to the right after landing.
  let arcX: number;
  let arcY: number;
  let tilt: number;

  if (frame <= landingFrame) {
    const progress = interpolate(frame, [0, landingFrame], [0, 1], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
      easing: Easing.inOut(Easing.ease),
    });
    arcX = interpolate(progress, [0, 1], [-0.12, 0.75]);
    const arcHeight = Math.sin(progress * Math.PI);
    arcY = 0.8 - arcHeight * 0.32;
    tilt = interpolate(progress, [0, 0.5, 1], [-10, 16, -6]);
  } else {
    const progress = interpolate(frame, [landingFrame, 90], [0, 1], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    });
    arcX = interpolate(progress, [0, 1], [0.75, 1.2]);
    arcY = 0.8 + Math.sin(progress * Math.PI * 3) * 0.008;
    tilt = interpolate(progress, [0, 1], [-6, 2]);
  }

  const bikeSize = Math.min(width, height) * 0.34;
  const bikeX = width * arcX;
  const bikeY = height * arcY;

  // Camera shake on landing impact.
  const shakeT = frame - landingFrame;
  const shake =
    shakeT >= 0 && shakeT < 10
      ? Math.sin(shakeT * 3) * (10 - shakeT) * 0.6
      : 0;

  const titleSpring = spring({ frame: frame - 8, fps, config: { damping: 11, stiffness: 180 } });
  const titleScale = interpolate(titleSpring, [0, 1], [2.2, 1]);
  const titleOpacity = interpolate(frame, [8, 16], [0, 1], { extrapolateRight: "clamp" });

  const subOpacity = interpolate(frame, [26, 36], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const subY = interpolate(frame, [26, 36], [20, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  const titleSize = vertical ? width * 0.16 : height * 0.16;
  const subSize = vertical ? width * 0.042 : height * 0.045;

  return (
    <AbsoluteFill
      style={{
        background:
          "linear-gradient(160deg, #0d1f0f 0%, #1c2b12 35%, #3b2a17 75%, #2a1d10 100%)",
        transform: `translate(${shake}px, ${shake * 0.4}px)`,
      }}
    >
      {/* subtle tree-line silhouettes */}
      <AbsoluteFill style={{ opacity: 0.35 }}>
        {new Array(7).fill(0).map((_, i) => {
          const x = (i / 6) * width - width * 0.05;
          const h = height * (0.18 + (i % 3) * 0.05);
          return (
            <div
              key={i}
              style={{
                position: "absolute",
                left: x,
                bottom: 0,
                width: width * 0.09,
                height: h,
                background: "#08140a",
                clipPath: "polygon(50% 0%, 0% 100%, 100% 100%)",
              }}
            />
          );
        })}
      </AbsoluteFill>

      <SpeedLines color={ACCENT} intensity={0.8} />

      {/* dirt ground */}
      <div
        style={{
          position: "absolute",
          bottom: 0,
          width: "100%",
          height: height * 0.16,
          background:
            "linear-gradient(180deg, rgba(61,43,31,0) 0%, #2a1d10 60%)",
        }}
      />

      <DustBurst
        triggerFrame={landingFrame}
        color="#c9b28a"
        originX={width * 0.75}
        originY={height * 0.8}
      />

      <div
        style={{
          position: "absolute",
          left: bikeX - bikeSize / 2,
          top: bikeY - bikeSize * 0.36,
          transform: `rotate(${tilt}deg)`,
          filter: "drop-shadow(0 18px 24px rgba(0,0,0,0.45))",
        }}
      >
        <MotoIcon color="#f5f5f0" size={bikeSize} />
      </div>

      <AbsoluteFill
        style={{
          justifyContent: "flex-start",
          alignItems: "center",
          flexDirection: "column",
          paddingTop: vertical ? height * 0.1 : height * 0.09,
        }}
      >
        <div
          style={{
            fontFamily: TheBoldFont,
            fontSize: titleSize,
            color: "#f5f5f0",
            letterSpacing: 4,
            opacity: titleOpacity,
            transform: `scale(${titleScale})`,
            textShadow: `0 0 40px ${ACCENT}55`,
          }}
        >
          SUR-RON
        </div>
        <div
          style={{
            fontFamily: "system-ui, sans-serif",
            fontWeight: 600,
            fontSize: subSize,
            color: ACCENT,
            opacity: subOpacity,
            transform: `translateY(${subY}px)`,
            marginTop: 12,
            letterSpacing: 1,
            textAlign: "center",
          }}
        >
          FUERA DE ASFALTO. SIN LÍMITES.
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
