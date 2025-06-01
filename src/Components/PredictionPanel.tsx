import React from "react";
import { Paper, Typography, Divider, Box } from "@mui/material";

interface DateObj {
  day: number;
  month: number;
  year: number;
}

interface WeatherSummary {
  ["month high"]: number;
  ["month low"]: number;
  ["month mean"]: number;
  ["total rain"]: number;
  ["most wind"]: number;
}

interface Props {
  prediction: number;
  country: string;
  date: DateObj;
  weather_summary: WeatherSummary;
  // Optional: add lat, lng, continent if you have them, or leave them out for now
  lat?: number;
  lng?: number;
  continent?: string;
}

const PredictionPanel: React.FC<Props> = ({
  prediction,
  country,
  date,
  weather_summary,
  lat,
  lng,
  continent,
}) => {
  // Format date as YYYY-MM-DD string for display
  const dateString = `${date.year}-${String(date.month).padStart(
    2,
    "0"
  )}-${String(date.day).padStart(2, "0")}`;

  const formatValue = (value: number | undefined | null, unit: string) => {
    return typeof value === "number" && !isNaN(value)
      ? `${value.toFixed(1)}${unit}`
      : `NaN${unit}`;
  };

  return (
    <Paper
      elevation={3}
      sx={{ position: "fixed", top: 100, right: 20, width: 350, p: 2 }}
    >
      <Typography variant="h6">Prediction Summary</Typography>
      <Divider sx={{ my: 1 }} />
      <Box sx={{ mb: 1 }}>
        {lat !== undefined && (
          <Typography>
            <strong>Latitude:</strong> {lat}
          </Typography>
        )}
        {lng !== undefined && (
          <Typography>
            <strong>Longitude:</strong> {lng}
          </Typography>
        )}
        <Typography>
          <strong>Country:</strong> {country}
        </Typography>
        {continent && (
          <Typography>
            <strong>Continent:</strong> {continent}
          </Typography>
        )}
        <Typography>
          <strong>Date:</strong> {dateString}
        </Typography>
      </Box>
      <Divider />
      <Box sx={{ my: 1 }}>
        <Typography>
          <strong>Daily High:</strong>{" "}
          {formatValue(weather_summary["month high"], "°C")}
        </Typography>
        <Typography>
          <strong>Daily Low:</strong>{" "}
          {formatValue(weather_summary["month low"], "°C")}
        </Typography>
        <Typography>
          <strong>Mean Temp:</strong>{" "}
          {formatValue(weather_summary["month mean"], "°C")}
        </Typography>
        <Typography>
          <strong>Total Rain:</strong>{" "}
          {formatValue(weather_summary["total rain"], " mm")}
        </Typography>
        <Typography>
          <strong>Most Wind:</strong>{" "}
          {formatValue(weather_summary["most wind"], " km/h")}
        </Typography>
      </Box>
      <Divider />
      <Typography
        sx={{ mt: 2 }}
        color="success.main"
        fontWeight="bold"
        variant="h6"
      >
        Prediction: {prediction.toFixed(2)}%
      </Typography>
    </Paper>
  );
};

export default PredictionPanel;
