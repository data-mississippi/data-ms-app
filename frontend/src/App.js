import React, { useState } from 'react'
import axios from 'axios'
import { MapContainer, TileLayer, Marker, Popup, CircleMarker, Tooltip, GeoJSON } from 'react-leaflet'
import statesGeoJSON from './us-states.json'
import 'leaflet/dist/leaflet.css'
import './App.css'
import './generated-styles.css'

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
      zoom={zoom} >
        <TileLayer
          url="https://{s}.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}{r}.png"
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright" target="_parent">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions" target="_parent">CARTO</a>'
        />
        {children}
      </MapContainer>
    )
}

function MapOfAmerica() {
  const view = {
    center: [37.8, -96], 
    zoom: 4
  }

  function getColor(d) {
    return d > 1000 ? '#800026' :
           d > 500  ? '#BD0026' :
           d > 200  ? '#E31A1C' :
           d > 100  ? '#FC4E2A' :
           d > 50   ? '#FD8D3C' :
           d > 20   ? '#FEB24C' :
           d > 10   ? '#FED976' :
                      '#FFEDA0';
  }

  function style(feature) {
    return {
        fillColor: getColor(feature.properties.density),
        weight: 2,
        opacity: 1,
        color: 'white',
        dashArray: '3',
        fillOpacity: 0.7
    };
  }

  return (
    <div>
    <GenericMap
      center={view.center}
      zoom={view.zoom}
    >
      <GeoJSON key='states-layer' data={statesGeoJSON} style={style} />
    </GenericMap>
    </div>
  )
}

function handleSubmit(event) {
  const text = document.querySelector('#char-input').value

  axios
    .get(`/char_count?text=${text}`).then(({data}) => {
      document.querySelector('#char-count').textContent = `${data.count} characters!`
    })
    .catch(err => console.log(err))
}



function MapOfForlorn() {
  return(
    <div className="max-w-md mx-auto flex p-6 h-full w-full">
        <MapContainer
          // placeholder={<MapPlaceholder />} 
          center={[34.256933, -88.703613]} 
          zoom={12}
        >
          <TileLayer
            attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          <CircleMarker 
            center={[34.27, -88.69]} 
            pathOptions={{ color: 'purple' }} 
            radius={11}
            permanent
          >
            <Tooltip direction="bottom" offset={[0, 20]} opacity={1} permanent>
              Greetings from Forlorn, Mississippi.
            </Tooltip>
          </CircleMarker>
        </MapContainer>
      </div>
  )
}

function Offering() {
  return (
    <div className="mt-24">
      <h2 className="text-2xl font-serif">OFFERING INSIDE</h2>
      <ul>
        <li className="font-mono text-purple-600"><a href="/?o=0">zero</a></li>
        {/* <li className="font-mono text-orange-600"><a href="/?o=1">one</a></li> */}
      </ul>
    </div>
  )
}

function GuideButton({onClick}) {
  return (
    <div className="flex items-end">
      <button 
        onClick={onClick}
        className="bg-orange-200 text-xl font-mono text-green-800 p-2 rounded-xl border-solid border-2 border-orange-300 mx-8 my-4">
        brain is a team of rivals
      </button>
    </div>
  )
}

function BrainIsATeamOfRivals({query}) {
  const [clicked, setClick] = useState(false)
  // const [o, setO] = useState(query.o)
  console.log(query.o)
  // if (query.o) {
  //   setO(query.o)
  // }

  function handleClick() {
    setClick(!clicked)
  }

  return (
    <div>
      {
        clicked ? 
        <Offering />
        : null
      }
      
      <div>
        { !query.o ? <GuideButton onClick={handleClick}/> :
          (query.o && query.o === '0') ?
          <div>
            <p className="font-mono">HOLY SPIRIT</p>
            <p>i'm here to talk about the things i've seen</p>
            <p className="font-mono text-purple-600"><a href="/?o=1">></a></p>
          </div>
            
          : 
          <div>
            <p className="font-mono">HOLY SPIRIT</p>
            <p>lord, ride my heart.</p>
            <p className="font-mono text-purple-600"><a href="/?o=0">></a></p>
          </div>
        }
      </div>
    </div>
  );
}

const getQueryParams = () => window.location.search.replace('?', '').split('&').reduce((r,e) => (r[e.split('=')[0]] = decodeURIComponent(e.split('=')[1]), r), {})

function App({props}) {
  console.log('app props ', props)
  const [query, setQuery] = useState(getQueryParams)

  return (
    <div className="App m-6">
      <div className="flex">
        <MapOfForlorn />
        <BrainIsATeamOfRivals query={query}/>
      </div>
      <div className="m-24" style={{width: '300px', height: '550px'}}>
        <MapOfAmerica />
      </div>
    </div>
  );
}

export default App;
