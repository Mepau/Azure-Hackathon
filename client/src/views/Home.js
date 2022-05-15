import React, { useState, useEffect } from "react";
import { Container, Row, Col } from "react-bootstrap";
import VideoPlayer from "../components/VideoPlayer";
import speechToText from "../utils/speechToText";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faMicrophone } from "@fortawesome/free-solid-svg-icons";

const Home = () => {
  const [urls, setUrls] = useState([]);
  const [displayText, setDisplaytext] = useState("");
  

  return (
    <Container>
      <Col>
        <Row md lg="3" className="justify-content-md-center">
          <span>
            <FontAwesomeIcon
              onClick={() => speechToText(setDisplaytext, setUrls)}
              size="lg"
              border
              icon={faMicrophone}
            />
            <span>Convert speech to text from your mic.</span>
          </span>
        </Row>

        <Row md lg="2" className="justify-content-md-center">
          <code style={{ fontSize: 50 }}>{displayText}</code>
        </Row>
        <Row
          style={{
            background:
              "linear-gradient(90deg, rgba(4,51,181,1) 0%, rgba(186,194,231,1) 50%, rgba(4,51,181,1) 100%)",
          }}
          md
          lg="2"
          className="justify-content-md-center"
        >
          <VideoPlayer urls={urls} setUrls={setUrls} />
        </Row>
      </Col>
    </Container>
  );
};

export default Home;
