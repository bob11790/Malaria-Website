import { useState } from "react";
import { MapContainer, TileLayer, Marker, useMapEvents } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import L from "leaflet";

// Fix default icon issues with Leaflet + React-Leaflet
delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png",
  iconUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png",
  shadowUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png",
});

function LocationMarker({ onClick }: { onClick: (latlng: L.LatLng) => void }) {
  // useMapEvents lets you listen to map events inside a component
  useMapEvents({
    click(e) {
      onClick(e.latlng);
    },
  });
  return null; // no UI here, just event handling
}

const normaliseLng = (lng: number) => {
  return ((((lng + 180) % 360) + 360) % 360) - 180;
};

const sendCoordinatesToBackend = async (coords: {
  lat: number;
  lng: number;
}) => {
  try {
    const response = await fetch("http://localhost:8000/coordinates", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(coords),
    });

    if (!response.ok) {
      throw new Error("Failed to send coordinates");
    }

    const data = await response.json();
    console.log("Server response:", data);
  } catch (error) {
    console.error(error);
  }
};

function ClickHandler() {
  useMapEvents({
    click(e) {
      const { lat, lng } = e.latlng;
      const normalizedLng = normaliseLng(lng);
      console.log("Clicked coordinates:", lat, normalizedLng);
      sendCoordinatesToBackend({ lat, lng: normalizedLng });
    },
  });

  return null;
}

const Map = () => {
  const [clickedPosition, setClickedPosition] = useState<L.LatLng | null>(null);

  return (
    <div
      style={{
        backgroundColor: "#b8bfbf",
        textAlign: "center",
        width: "100%",
        height: "100vh",
        paddingTop: 20,
      }}
    >
      <MapContainer
        center={[51.505, -0.09]}
        zoom={13}
        style={{
          height: "500px",
          width: "100%",
          maxWidth: "800px",
          margin: "auto",
        }}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        />
        {/* Attach the click handler */}
        <LocationMarker onClick={(latlng) => setClickedPosition(latlng)} />

        {/* If we have a clicked position, render a marker */}
        {clickedPosition && <Marker position={clickedPosition} />}
        <ClickHandler />
      </MapContainer>

      {/* Display clicked coordinates */}
      {clickedPosition && (
        <div style={{ marginTop: 10, color: "#333" }}>
          Clicked location: Latitude: {clickedPosition.lat.toFixed(5)},
          Longitude: {normaliseLng(clickedPosition.lng).toFixed(5)}
        </div>
      )}
    </div>
  );
};

export default Map;
