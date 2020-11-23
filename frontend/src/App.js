import React, { useState, useEffect } from 'react'
import axios from 'axios'
import { MapContainer, TileLayer, Marker, Popup, CircleMarker, Tooltip, GeoJSON } from 'react-leaflet'
// import statesGeoJSON from './us-states.geojson'
// import msCountiesGeoJson from './ms-counties.json'
// import msPrecinctsGeoJson from './ms-precincts-12.json'
import testJson from './test.json'
import 'leaflet/dist/leaflet.css'
import './App.css'
import './generated-styles.css'
import GreetingsFromForlorn from './GreetingsFromForlorn'

// function MapPlaceholder(message) {
//   return (
//     <div>
//     <p>{message ? message : 'The map is not working with your browser.'}</p>
//     <p><noscript>You need to enable JavaScript to see this map.</noscript></p>
//   )
// }

// // Map of Forlorn, Mississippi.{' '}

// <GeoJSON key='watershed-layer' data={this.props.geojson} style={this.getStyle} />

 // const MapPlaceholder = (<MapPlaceholder message={'Map of America.'} />)

function GenericMap({ center, zoom, children }) {
  return (
    <MapContainer
      center={center} 
      zoom={zoom}
      className=""
      >
        <TileLayer
          url="https://{s}.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}{r}.png"
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright" target="_parent">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions" target="_parent">CARTO</a>'
        />
        {children}
    </MapContainer>
    )
}

function getCounties() {
  axios.get(`/counties/`, {
    headers: {
      'Accept': 'application/json'
  }
  }).then(({data}) => {
      return data
    }).catch(err => console.log(err))
}

function getRedChoroplethStyle(feature) {
  function setDensityColor(d) {
    return d > 1000 ? '#800026' :
           d > 500  ? '#BD0026' :
           d > 200  ? '#E31A1C' :
           d > 100  ? '#FC4E2A' :
           d > 50   ? '#FD8D3C' :
           d > 20   ? '#FEB24C' :
           d > 10   ? '#FED976' :
                      '#FFEDA0';
  }

  return {
      fillColor: setDensityColor(feature.properties.density),
      weight: 1,
      opacity: 1,
      color: '#666',
      dashArray: '3',
      fillOpacity: 0.7
  };
}

const choroplethStyle = function getRedChoroplethStyle(feature) {
  function setDensityColor(d) {
    return d > 1000 ? '#800026' :
           d > 500  ? '#BD0026' :
           d > 200  ? '#E31A1C' :
           d > 100  ? '#FC4E2A' :
           d > 50   ? '#FD8D3C' :
           d > 20   ? '#FEB24C' :
           d > 10   ? '#FED976' :
                      '#FFEDA0';
  }

  return {
      fillColor: setDensityColor(feature.properties.density),
      weight: 1,
      opacity: 1,
      color: '#666',
      dashArray: '3',
      fillOpacity: 0.7
  };
}

function getGeoJsonPerCounty(countiesGeo, countyFips) {
  countiesGeo.features.map((feature) => {
    console.log(feature.properties)
    if (feature.properties.COUNTYFP10 == countyFips) {
      console.log("true,", feature)
      return feature
    }
  })
}

// county geojson guide? https://sampleserver6.arcgisonline.com/arcgis/rest/services/Census/MapServer/layers

function MapOfAmerica() {
  const america = {center: [37.8, -96], zoom: 3.5}
  const mississippiView = {center: [34.256933, -88.703613], zoom: 9}
  const [view, setView] = useState(mississippiView)
  const [boundary, setBoundary] = useState(null)

  function mouseoverBoundary(e) {
    const layer = e.target

    const layerFeature = (layer && layer.feature && layer.feature.properties) 
                          ? layer.feature.properties 
                          : null

    setBoundary(() => layerFeature)

    layer.setStyle({
      fillOpacity: 1,
    });
  }

  function resetBoundaryStyle(e) {
    // get the original style from this.feature aka the <GeoJSON /> instance
    const originalStyle = getRedChoroplethStyle(this.feature)

    e.target.setStyle({
      fillOpacity: originalStyle.fillOpacity
    })
  }

  function handleClick(e) {
    console.log('click')
    console.log(e)
  }

  function eventHandlersOnEachFeature(feature, layer) {
    // this doesn't seem right...
    // update: it's not! see https://reactjs.org/docs/refs-and-the-dom.html
    // or maybe it is? see node_modules/@types/leaflet/index.d.ts line 1209

    layer.on({
      // mouseover: mouseoverBoundary,
      // mouseout: resetBoundaryStyle,
      // click: handleClick
    })
  }

  return (
    <div className="w-1/2">
      <div>
        {boundary ? 
        <h2>
          {boundary.name}
        </h2> 
        : null}
      </div>
      <GenericMap
        center={view.center}
        zoom={view.zoom}
      >
        {/* <GeoJSON 
          key='states-layer' 
          data={msPrecinctsGeoJson} 
          //style={choroplethStyle} 
          //onEachFeature={eventHandlersOnEachFeature}
        /> */}
        <Tooltip direction="bottom" offset={[0, 20]} opacity={1} permanent>
          permanent Tooltip for Rectangle
        </Tooltip>
      </GenericMap>
    </div>
  )
}

function App() {
  const [counties, setCounties] = useState(null)

  useEffect(() => {
    fetch(`/counties/`, {
      headers: {'Accept': 'application/json'}
    }).then((res) => res.json())
      .then((counties) => {
        console.log(counties)
        setCounties(counties)
      })
    // const counties = getCounties()
    // console.log(counties)
    // setCounties(counties)
  }, [setCounties])
  return (
    <div className="flex flex-wrap md items-center h-screen p-24">
      <MapOfAmerica />
      <div>
        {counties &&
          <ul>
            {counties.map(county => {
              return <li>{county.name} | {county.fips}</li>
            })}
          </ul>
        }
      </div>
      
    </div>
  );
}

export default App;
