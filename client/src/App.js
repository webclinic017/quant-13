import React from "react";
import { createGlobalStyle, ThemeProvider } from "styled-components";
import StyledNavbar from "./Components/Navbar";
import StyledFooter from "./Components/Footer";
import StyledContent from "./Components/Content";
import Bungee from "./assets/Bungee-Regular.ttf";
import Roboto from "./assets/Roboto-Regular.ttf";
import { BrowserRouter as Router, Switch, Route, Link } from "react-router-dom";

const theme = {
  primary: "#F3EBE9",
  secondary: "#CAA892",
  secDark: "#7B707A",
  white: "#fffff4",
  textFont: "roboto,sans-seriff",
  titleFont: "bungee,sans-seriff",
  navheight: "3.5rem",
  footheight: "10vh",
  boxShadow: "0px 4px 4px 0px rgba(0, 0, 0, 0.25)",
};
const GlobalStyle = createGlobalStyle`
@font-face {
    font-family: 'Bungee';
    src: url(${Bungee}) format('truetype');
    font-weight: 300;
    font-style: normal;
    font-display: auto;
  }
  @font-face {
    font-family: 'Roboto';
    src: url(${Roboto}) format('truetype');
    font-weight: 300;
    font-style: normal;
    font-display: auto;
  }
body {
    background-color: ${(props) => props.theme.white};
    
  }
`;

function App() {
  return (
    <ThemeProvider theme={theme}>
      <Router>
        <GlobalStyle />
        <StyledNavbar />
        <StyledContent />
        <StyledFooter />
      </Router>
    </ThemeProvider>
  );
}

export default App;
