import ReactPlayer from "react-player";

const VideoPlayer = (props) => {
  const { url } = props;
  return (
    <div className="player-wrapper">
      <ReactPlayer
        className="react-player"
        url={url}
        width="100%"
        height="100%"
        playing={true}
        controls
        muted={true}
      />
    </div>
  );
};

export default VideoPlayer;
