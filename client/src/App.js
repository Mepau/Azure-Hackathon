import React, { Component } from "react";
import { Container } from "react-bootstrap";
import { getTokenOrRefresh } from "./token_utils";
import { ResultReason } from "microsoft-cognitiveservices-speech-sdk";

const sdk = require("microsoft-cognitiveservices-speech-sdk");

export default class App extends Component {
  constructor(props) {
    super(props);

    this.state = {
      displayText: "INITIALIZED: ready to test speech...",
    };
  }

  async componentDidMount() {
    // check for valid speech key/region
    const tokenRes = await getTokenOrRefresh();
    if (tokenRes.authToken === null) {
      this.setState({
        displayText: "FATAL_ERROR: " + tokenRes.error,
      });
    }
  }

  async sttFromMic() {
    const tokenObj = await getTokenOrRefresh();
    const speechConfig = sdk.SpeechConfig.fromAuthorizationToken(
      tokenObj.authToken,
      tokenObj.region
    );
    speechConfig.speechRecognitionLanguage = "es-DO";

    const audioConfig = sdk.AudioConfig.fromDefaultMicrophoneInput();
    const recognizer = new sdk.SpeechRecognizer(
      speechConfig,
      audioConfig
    );

    this.setState({
      displayText: "speak into your microphone...",
    });

    recognizer.recognized = (s, e) => {
      if (e.result.reason === sdk.ResultReason.NoMatch) {
        const noMatchDetail = sdk.NoMatchDetails.fromResult(e.result);
        console.log(
          "(recognized)  Reason: " +
            sdk.ResultReason[e.result.reason] +
            " | NoMatchReason: " +
            sdk.NoMatchReason[noMatchDetail.reason]
        );
      } else {
        console.log(
          `(recognized)  Reason: ${
            sdk.ResultReason[e.result.reason]
          } | Duration: ${e.result.duration} | Offset: ${e.result.offset}`
        );
        console.log(`Text: ${e.result.text}`);
      }
    };

    recognizer.canceled = (s, e) => {
      let str = "(cancel) Reason: " + sdk.CancellationReason[e.reason];
      if (e.reason === sdk.CancellationReason.Error) {
        str += ": " + e.errorDetails;
      }
      console.log(str);
    };

    recognizer.speechEndDetected = (s, e) => {
      console.log(`(speechEndDetected) SessionId: ${e.sessionId}`);
      recognizer.close();
    };

    recognizer.startContinuousRecognitionAsync(
      () => {
        console.log("Recognition started");
      },
      (err) => {
        console.trace("err - " + err);
        recognizer.close();
      }
    );

    //recognizer.startContinuousRecognitionAsync((result) => {
    //  console.log(ResultReason.RecognizedSpeech);
    //  let displayText;
    //  if (result.reason === ResultReason.RecognizedSpeech) {
    //    displayText = `RECOGNIZED: Text=${result.text}`;
    //  } else {
    //    displayText =
    //      "ERROR: Speech was cancelled or could not be recognized. Ensure your microphone is working properly.";
    //  }
//
    //  this.setState({
    //    displayText: displayText,
    //  });
    //});
  }

  async fileChange(event) {
    const audioFile = event.target.files[0];
    console.log(audioFile);
    const fileInfo = audioFile.name + ` size=${audioFile.size} bytes `;

    this.setState({
      displayText: fileInfo,
    });

    const tokenObj = await getTokenOrRefresh();
    const speechConfig = sdk.SpeechConfig.fromAuthorizationToken(
      tokenObj.authToken,
      tokenObj.region
    );
    speechConfig.speechRecognitionLanguage = "en-US";

    const audioConfig = sdk.AudioConfig.fromWavFileInput(audioFile);
    const recognizer = new sdk.SpeechRecognizer(
      speechConfig,
      audioConfig
    );

    recognizer.recognizeOnceAsync((result) => {
      let displayText;
      if (result.reason === ResultReason.RecognizedSpeech) {
        displayText = `RECOGNIZED: Text=${result.text}`;
      } else {
        displayText =
          "ERROR: Speech was cancelled or could not be recognized. Ensure your microphone is working properly.";
      }

      this.setState({
        displayText: fileInfo + displayText,
      });
    });
  }

  render() {
    return (
      <Container className="app-container">
        <h1 className="display-4 mb-3">Speech sample app</h1>

        <div className="row main-container">
          <div className="col-6">
            <i
              className="fas fa-microphone fa-lg mr-2"
              onClick={() => this.sttFromMic()}
            >
              MIC
            </i>
            Convert speech to text from your mic.
            <div className="mt-2">
              <label htmlFor="audio-file">
                <i className="fas fa-file-audio fa-lg mr-2"></i>
              </label>
              <input
                type="file"
                id="audio-file"
                onChange={(e) => this.fileChange(e)}
                style={{ display: "none" }}
              />
              Convert speech to text from an audio file.
            </div>
          </div>
          <div className="col-6 output-display rounded">
            <code>{this.state.displayText}</code>
          </div>
        </div>
      </Container>
    );
  }
}

