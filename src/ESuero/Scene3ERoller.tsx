import React from "react";
import { AbsoluteFill, interpolate, staticFile, useCurrentFrame } from "remotion";
import { PhotoScene } from "./PhotoScene";

const CROSS_START = 50;
const CROSS_END = 65;

export const Scene3ERoller: React.FC = () => {
  const frame = useCurrentFrame();
  const frontOpacity = interpolate(frame, [CROSS_START, CROSS_END], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill>
      <PhotoScene
        src={staticFile("photos/e-roller-side.jpg")}
        zoomFrom={1}
        zoomTo={1.12}
        panXFrom={0}
        panXTo={2}
      />
      <AbsoluteFill style={{ opacity: frontOpacity }}>
        <PhotoScene
          src={staticFile("photos/e-roller-front.jpg")}
          zoomFrom={1.03}
          zoomTo={1.14}
          panYFrom={0}
          panYTo={-1.5}
        />
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
