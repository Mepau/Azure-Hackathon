import React, { useState, useEffect } from "react";
import { Container, Row } from "react-bootstrap";
import VideoPlayer from "../components/VideoPlayer";
import speechToText from "../utils/speechToText";

const Home = () => {
  const [urls, setUrls] = useState([]);
  const [displayText, setDisplaytext] = useState("");

  return (
    <Container>
      <Row>
        <h1 className="display-4 mb-3">Speech sample app</h1>

        <div className="row main-container">
          <div className="col-6">
            <i
              className="fas fa-microphone fa-lg mr-2"
              onClick={() => speechToText(setDisplaytext, urls,setUrls)}
            >
              MIC
            </i>
            Convert speech to text from your mic.
          </div>
          <div className="col-6 output-display rounded">
            <code>{displayText}</code>
          </div>
        </div>
      </Row>
      <Row>
        <VideoPlayer urls={urls} setUrls={setUrls} />
      </Row>
    </Container>
  );
};

export default Home;
