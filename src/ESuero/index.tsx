import React, { useEffect, useState } from "react";
import {
  AbsoluteFill,
  Sequence,
  continueRender,
  delayRender,
  interpolate,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { Scene1SurRon } from "./Scene1SurRon";
import { Scene2Scooter } from "./Scene2Scooter";
import { Scene3ERoller } from "./Scene3ERoller";
import { Outro } from "./Outro";
import { BrandBadge } from "./BrandBadge";
import { loadFont } from "../load-font";

export const SCENE_DURATION = 90; // 3s @ 30fps
export const OUTRO_DURATION = 60; // 2s @ 30fps
export const FADE_DURATION = 12;
export const ESUERO_TOTAL_DURATION = SCENE_DURATION * 3 + OUTRO_DURATION;
export const ESUERO_FPS = 30;

const CrossFade: React.FC<{ children: React.ReactNode; duration: number }> = ({
  children,
  duration,
}) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const opacity = interpolate(
    frame,
    [0, duration, durationInFrames - duration, durationInFrames],
    [0, 1, 1, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
  );
  return <AbsoluteFill style={{ opacity }}>{children}</AbsoluteFill>;
};

export const ESuero: React.FC = () => {
  const { width, height } = useVideoConfig();
  const vertical = height >= width;
  const [fontReady, setFontReady] = useState(false);

  useEffect(() => {
    const handle = delayRender();
    loadFont()
      .then(() => setFontReady(true))
      .finally(() => continueRender(handle));
  }, []);

  if (!fontReady) {
    return <AbsoluteFill style={{ background: "#0b0b0d" }} />;
  }

  return (
    <AbsoluteFill style={{ background: "#0b0b0d" }}>
      <Sequence durationInFrames={SCENE_DURATION}>
        <CrossFade duration={FADE_DURATION}>
          <Scene1SurRon />
        </CrossFade>
      </Sequence>

      <Sequence from={SCENE_DURATION} durationInFrames={SCENE_DURATION}>
        <CrossFade duration={FADE_DURATION}>
          <Scene2Scooter />
        </CrossFade>
      </Sequence>

      <Sequence from={SCENE_DURATION * 2} durationInFrames={SCENE_DURATION}>
        <CrossFade duration={FADE_DURATION}>
          <Scene3ERoller />
        </CrossFade>
      </Sequence>

      <Sequence from={SCENE_DURATION * 3} durationInFrames={OUTRO_DURATION}>
        <CrossFade duration={FADE_DURATION}>
          <Outro vertical={vertical} />
        </CrossFade>
      </Sequence>

      <BrandBadge hideAfter={SCENE_DURATION * 3} scale={width} />
    </AbsoluteFill>
  );
};
