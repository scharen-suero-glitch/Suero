import React from "react";
import { AbsoluteFill, Img, interpolate, useCurrentFrame, useVideoConfig } from "remotion";

// Real product/action photos are square-ish and must work in both a 16:9
// and a 9:16 composition without cropping the subject: a blurred, darkened
// cover-fit copy fills the frame, and a sharp contain-fit copy — carrying
// the actual Ken Burns pan/zoom — sits on top, fully visible either way.
export const PhotoScene: React.FC<{
  src: string;
  zoomFrom?: number;
  zoomTo?: number;
  panXFrom?: number;
  panXTo?: number;
  panYFrom?: number;
  panYTo?: number;
}> = ({
  src,
  zoomFrom = 1,
  zoomTo = 1.08,
  panXFrom = 0,
  panXTo = 0,
  panYFrom = 0,
  panYTo = 0,
}) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const t = interpolate(frame, [0, durationInFrames], [0, 1], {
    extrapolateRight: "clamp",
  });
  const zoom = interpolate(t, [0, 1], [zoomFrom, zoomTo]);
  const panX = interpolate(t, [0, 1], [panXFrom, panXTo]);
  const panY = interpolate(t, [0, 1], [panYFrom, panYTo]);

  return (
    <AbsoluteFill>
      <AbsoluteFill>
        <Img
          src={src}
          style={{
            width: "100%",
            height: "100%",
            objectFit: "cover",
            filter: "blur(60px) brightness(0.5) saturate(1.15)",
            transform: "scale(1.2)",
          }}
        />
      </AbsoluteFill>
      <AbsoluteFill
        style={{
          background:
            "linear-gradient(180deg, rgba(0,0,0,0.2) 0%, rgba(0,0,0,0.05) 45%, rgba(0,0,0,0.55) 100%)",
        }}
      />
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center" }}>
        <Img
          src={src}
          style={{
            maxWidth: "94%",
            maxHeight: "84%",
            objectFit: "contain",
            transform: `scale(${zoom}) translate(${panX}%, ${panY}%)`,
            filter: "drop-shadow(0 30px 50px rgba(0,0,0,0.55))",
          }}
        />
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
