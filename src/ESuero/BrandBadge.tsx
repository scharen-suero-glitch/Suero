import React from "react";
import { interpolate, useCurrentFrame } from "remotion";
import { TheBoldFont } from "../load-font";

export const BrandBadge: React.FC<{ hideAfter: number; scale: number }> = ({
  hideAfter,
  scale,
}) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(
    frame,
    [10, 22, hideAfter - 12, hideAfter],
    [0, 1, 1, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
  );

  if (opacity <= 0) {
    return null;
  }

  return (
    <div
      style={{
        position: "absolute",
        top: scale * 0.055,
        left: scale * 0.055,
        padding: `${scale * 0.016}px ${scale * 0.028}px`,
        borderRadius: 999,
        background: "rgba(10,10,10,0.5)",
        opacity,
      }}
    >
      <span
        style={{
          fontFamily: TheBoldFont,
          color: "#fff",
          fontSize: scale * 0.026,
          letterSpacing: 1,
        }}
      >
        E-SUERO
      </span>
    </div>
  );
};
