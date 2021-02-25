import React from 'react'
import { MapContainer, TileLayer } from 'react-leaflet'
import 'leaflet/dist/leaflet.css'
import '../styles/App.css'
import '../styles/generated-styles.css'

// todo
function MapPlaceholder(message) {
  return (
    <div>
    <p>{message ? message : 'The map is not working with your browser.'}</p>
    <p><noscript>You need to enable JavaScript to see this map.</noscript></p>
    </div>
  )
}

function BaseMap({ center, zoom, className, children }) {
    return (
      <MapContainer
        center={center} 
        zoom={zoom}
        className={className}
        >
          <TileLayer
            url="https://{s}.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}{r}.png"
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright" target="_parent">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions" target="_parent">CARTO</a>'
          />
          {children}
      </MapContainer>
    )
}

export default BaseMap
