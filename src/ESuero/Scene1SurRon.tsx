import React from "react";
import { AbsoluteFill, interpolate, staticFile, useCurrentFrame } from "remotion";
import { PhotoScene } from "./PhotoScene";

export const Scene1SurRon: React.FC = () => {
  const frame = useCurrentFrame();
  // Punchy impact pulse + subtle handheld shake for hook energy.
  const punch = interpolate(frame, [16, 20, 26], [1, 1.05, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const shakeX = Math.sin(frame * 1.3) * 1.5;
  const shakeY = Math.cos(frame * 1.7) * 1.2;

  return (
    <AbsoluteFill
      style={{ transform: `scale(${punch}) translate(${shakeX}px, ${shakeY}px)` }}
    >
      <PhotoScene
        src={staticFile("photos/sur-ron.jpg")}
        zoomFrom={1.05}
        zoomTo={1.2}
        panXFrom={0}
        panXTo={-2}
        panYFrom={1}
        panYTo={-1.5}
      />
    </AbsoluteFill>
  );
};
