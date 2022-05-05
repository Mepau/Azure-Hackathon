import React, { Component } from "react";
import { getTokenOrRefresh } from "./utils/token_utils";
import Home from "./views/Home";

export default class App extends Component {
  constructor(props) {
    super(props);

    this.state = {
      displayText: "INITIALIZED: ready to test speech..."
    };
  }

  async componentDidMount() {
    // check for valid speech key/region
    const tokenRes =  getTokenOrRefresh();
    if (tokenRes.authToken === null) {
      this.setState({
        displayText: "FATAL_ERROR: " + tokenRes.error,
      });
    }
  }

  render() {
    return (
    <div>
      <h2>{this.state.displayText}</h2>
      <Home />
      </div>);
  }
}
