import axios from "axios";
import { getTokenOrRefresh } from "../utils/token_utils";
import jsonUrls from "../urls.json";

const sdk = require("microsoft-cognitiveservices-speech-sdk");

export default async function speechToText(setDisplaytext, setUrls) {
  const tokenObj = await getTokenOrRefresh();
  const speechConfig = sdk.SpeechConfig.fromAuthorizationToken(
    tokenObj.authToken,
    tokenObj.region
  );
  speechConfig.speechRecognitionLanguage = "es-DO";

  const audioConfig = sdk.AudioConfig.fromDefaultMicrophoneInput();
  const recognizer = new sdk.SpeechRecognizer(speechConfig, audioConfig);

  setDisplaytext("speak into your microphone...");

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
      setDisplaytext(e.result.text);

      if(e.result.text.includes("Parar micrófono")){
        recognizer.stopContinuousRecognitionAsync()
        recognizer.close()
      }
      axios
        .post(jsonUrls.aiFunctionUrl, {
          sentence: e.result.text,
        })
        .then((res) => {
          if (res.data.length > 0)
            setUrls((prevUrls) => {
              return [...prevUrls, ...JSON.parse(res.data.replace(/'/g, '"'))];
            });
        });
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
}
