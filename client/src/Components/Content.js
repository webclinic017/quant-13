import React from "react";
import styled from "styled-components";
import Test from "../assets/wide-cafe.jpg";
import { BrowserRouter as Router, Switch, Route, Link } from "react-router-dom";

const StyledContent = styled(ContentPage)`
  .bg-img {
    background: url(${process.env.PUBLIC_URL + Test});
    margin-left: 0;
    margin-top: calc(${(props) => props.theme.navheight} + 1rem);
    margin-bottom: ${(props) => props.theme.footheight};
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    height: calc(
      100vh - 1rem
        ${(props) => {
          return " - " + props.theme.navheight + " - " + props.theme.footheight;
        }}
    );
    background-size: 75vw 100%;
    clip-path: circle(50% at 0 90%);
  }
`;
const StyledEmptyPage = styled(EmptyPage)`
  margin-top: calc(${(props) => props.theme.navheight} + 1rem);
  display: grid;
  grid-template-columns: 45% 5% 30% auto;
  grid-template-rows: 20% 10% 10% auto;
  height: calc(
    100vh - 1rem
      ${(props) => {
        return " - " + props.theme.navheight + " - " + props.theme.footheight;
      }}
  );

  .hd {
    font-family: ${(props) => props.theme.textFont};
    grid-row: 2/3;
    grid-column: 2/4;
    text-decoration: underline;
  }
  .TextBlock {
    font-family: ${(props) => props.theme.textFont};
    grid-row: 3/4;
    grid-column: 2/4;
  }
`;

function ContentPage(props) {
  return (
    <div className={props.className}>
      <div className="bg-img"></div>
      <Switch>
        <Route exact path="/">
          <StyledEmptyPage Text="Home" />
        </Route>
        <Route path="/about">
          <StyledEmptyPage Text="About" />
        </Route>
      </Switch>
    </div>
  );
}
function EmptyPage(props) {
  return (
    <div className={props.className}>
      <h1 className="hd">Website für Gesselschaftsspiele</h1>
      <div className="TextBlock">{props.Text}</div>
    </div>
  );
}

export default StyledContent;
