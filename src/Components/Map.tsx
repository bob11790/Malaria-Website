import { useState } from "react";
import { MapContainer, TileLayer, Marker, useMapEvents } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import L from "leaflet";

delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png",
  iconUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png",
  shadowUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png",
});

const normaliseLng = (lng: number) => {
  return ((((lng + 180) % 360) + 360) % 360) - 180;
};

const sendCoordinatesToBackend = async (coords: {
  lat: number;
  lng: number;
  country: string;
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

function ClickHandler({
  setClickedPosition,
  setClickedCountry,
}: {
  setClickedPosition: (pos: L.LatLng) => void;
  setClickedCountry: (country: string) => void;
}) {
  useMapEvents({
    click: async (e) => {
      const { lat, lng } = e.latlng;
      const normalizedLng = normaliseLng(lng);

      setClickedPosition(e.latlng);
      console.log("Clicked coordinates:", lat, normalizedLng);

      try {
        const response = await fetch(
          `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${normalizedLng}`
        );
        const data = await response.json();
        const country = data?.address?.country || "Unknown";

        setClickedCountry(country);
        sendCoordinatesToBackend({ lat, lng: normalizedLng, country });
      } catch (err) {
        console.error("Reverse geocoding failed:", err);
      }
    },
  });

  return null;
}

const Map = () => {
  const [clickedPosition, setClickedPosition] = useState<L.LatLng | null>(null);
  const [clickedCountry, setClickedCountry] = useState<string | null>(null);

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
        {/* Unified Click Handler */}
        <ClickHandler
          setClickedPosition={setClickedPosition}
          setClickedCountry={setClickedCountry}
        />
        {clickedPosition && <Marker position={clickedPosition} />}
      </MapContainer>

      {clickedPosition && (
        <div style={{ marginTop: 10, color: "#333" }}>
          Clicked location: Latitude: {clickedPosition.lat.toFixed(5)},
          Longitude: {normaliseLng(clickedPosition.lng).toFixed(5)} <br />
          Country: {clickedCountry || "Loading..."}
        </div>
      )}
    </div>
  );
};

export default Map;
