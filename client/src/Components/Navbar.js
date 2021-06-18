import React from "react";
import styled from "styled-components";
import { Link } from "react-router-dom";

import { ReactComponent as ChessLogo } from "../assets/chess-figure.svg";

const StyledLink = styled(Link)`
  color: inherit;
  text-decoration: inherit;

  &:focus,
  &:hover,
  &:visited,
  &:link,
  &:active {
    text-decoration: none;
  }
`;

const StyledNavbar = styled(Navbar)`
  background-color: ${(props) => props.theme.white};
  position: fixed;
  left: 0;
  top: 0;
  height: ${(props) => props.theme.navheight};
  width: 100%;
  display: flex;
  .nNavbar {
    display: flex;
    padding: 0px 1.3vw;
    justify-content: space-between;
    align-items: center;
    width: 100vw;
  }
  .left {
    display: flex;
    align-items: center;
    justify-content: flex-start;
  }
  .navLinks {
    display: flex;
    flex: 0 0 auto;
    align-items: center;
    margin-right: 1.5vw;
  }
  .icon {
    width: 2rem;
    height: 2rem;
  }
  .right {
    display: flex;
    align-items: center;
    justify-content: flex-end;
  }
  .logoBlock {
    background: white;
    margin-right: 2vw;
    height: 2.5rem;
    padding: 0 5px 0 0;
    display: flex;
    align-items: center;
    border-radius: 0.7rem 0.1rem;
    box-shadow: 0px 4px 4px 0px rgba(0, 0, 0, 0.25);
    :hover {
      cursor: pointer;
    }
  }
  .logoText {
  }
`;

const StyledItem = styled(Item)`
  font-family: ${(props) => props.theme.titleFont};
  flex: 0 0 auto;
  margin-right: 1.5vw;
  font-family: ${(props) => props.theme.titleFont}, sans-serif;
  border-radius: 0.7rem 0.1rem;
  padding: 0 0.2rem;
  :hover {
    background-color: ${(props) => props.theme.primary};
    cursor: pointer;
    box-shadow: ${(props) => props.theme.boxShadow};
  }
`;

function Navbar(props) {
  return (
    <div className={props.className}>
      <div className="nNavbar">
        <div className="left">
          <div className="logoBlock">
            <ChessLogo className="icon" href="/" />
            <div className="logoText">
              <StyledLink to="/">Home</StyledLink>
            </div>
          </div>
          <div className="navLinks">
            {Array(5)
              .fill(1)
              .map((el, i) => (
                <StyledItem key={i} number={i} content={"Hello"} />
              ))}
          </div>
        </div>
        <div className="right">
          {Array(3)
            .fill(1)
            .map((el, i) => (
              <StyledItem key={i} number={i} content={"End"} />
            ))}
        </div>
      </div>
    </div>
  );
}

function Item(props) {
  return (
    <div className={props.className}>
      <StyledLink to="/about" style={{ textDecoration: "none" }}>
        {props.content}
      </StyledLink>
    </div>
  );
}

export default StyledNavbar;
