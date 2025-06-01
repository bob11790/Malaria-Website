import React from "react";
import { AppBar, Toolbar, Typography } from "@mui/material";

const Header: React.FC = () => (
  <AppBar position="static" color="primary">
    <Toolbar>
      <Typography variant="h6" component="div">
        Maleria Prediction Map
      </Typography>
    </Toolbar>
  </AppBar>
);

export default Header;
