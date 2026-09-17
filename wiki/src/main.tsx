import React from "react";
import { createRoot } from "react-dom/client";
import App from "./App";
import "./styles.css";
import "./canvas.css";
import "./world/world.css";
import "./visual/theme.css";
import { SignalProvider } from "./visual/SignalState";
createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <SignalProvider>
      <App />
    </SignalProvider>
  </React.StrictMode>,
);
