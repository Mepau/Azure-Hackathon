import React, { Component } from "react";
import { Container, Col, Row } from "react-bootstrap";
import { getTokenOrRefresh } from "./utils/token_utils";
import Home from "./views/Home";

export default class App extends Component {
  constructor(props) {
    super(props);

    this.state = {
      displayText: "INITIALIZED: ready to translate speech...",
    };
  }

  async componentDidMount() {
    // check for valid speech key/region
    const tokenRes = getTokenOrRefresh();
    if (tokenRes.authToken === null) {
      this.setState({
        displayText: "FATAL_ERROR: " + tokenRes.error,
      });
    }
  }

  render() {
    return (
      <div style={{ background: "linear-gradient(90deg, rgba(4,51,181,1) 0%, rgba(186,194,231,1) 50%, rgba(4,51,181,1) 100%)" }}>
        <Col className="justify-content-md-center">
        <Row md lg="2"  className="justify-content-md-center">
          <h2 className="display-4 mb-3">Speech to sign app</h2>
        </Row>
          <Row cxs lg="2" className="justify-content-md-center">
            <h3>{this.state.displayText}</h3>
          </Row>
          <Row className="justify-content-md-center">
            <Home />
          </Row>
        </Col>
      </div>
    );
  }
}
