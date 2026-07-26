import React from "react";
import { AbsoluteFill, staticFile } from "remotion";
import { PhotoScene } from "./PhotoScene";

export const Scene2Scooter: React.FC = () => {
  return (
    <AbsoluteFill>
      <PhotoScene
        src={staticFile("photos/e-scooter.jpg")}
        zoomFrom={1.1}
        zoomTo={1}
        panXFrom={-1.5}
        panXTo={1}
        panYFrom={0.5}
        panYTo={-0.5}
      />
    </AbsoluteFill>
  );
};
