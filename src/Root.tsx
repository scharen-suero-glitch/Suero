import "./index.css";
import { Composition, staticFile } from "remotion";
import {
  CaptionedVideo,
  calculateCaptionedVideoMetadata,
  captionedVideoSchema,
} from "./CaptionedVideo";
import { ESuero, ESUERO_FPS, ESUERO_TOTAL_DURATION } from "./ESuero";

// Each <Composition> is an entry in the sidebar!

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="CaptionedVideo"
        component={CaptionedVideo}
        calculateMetadata={calculateCaptionedVideoMetadata}
        schema={captionedVideoSchema}
        width={1080}
        height={1920}
        defaultProps={{
          src: staticFile("sample-video.mp4"),
        }}
      />
      <Composition
        id="ESuero-Mobile"
        component={ESuero}
        durationInFrames={ESUERO_TOTAL_DURATION}
        fps={ESUERO_FPS}
        width={1080}
        height={1920}
      />
      <Composition
        id="ESuero-Desktop"
        component={ESuero}
        durationInFrames={ESUERO_TOTAL_DURATION}
        fps={ESUERO_FPS}
        width={1920}
        height={1080}
      />
    </>
  );
};
