import { useState } from "react";
import ReactPlayer from "react-player";

const VideoPlayer = (props) => {

  const { urls, setUrls } = props;
  const [ counter, setCounter] = useState(0)


  const loadNextVideo = () => {

    setUrls(urls.slice(1))
    //Force rendering by "changing" state
    setCounter(0)
  }

  return (
    <div className="player-wrapper">
      <ReactPlayer
        className="react-player"
        url={urls[counter]}
        width="100%"
        height="100%"
        playing={true}
        controls
        muted={true}
        onEnded={()=> loadNextVideo()}
      />
    </div>
  );
};

export default VideoPlayer;
