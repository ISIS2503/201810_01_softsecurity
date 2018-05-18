import { Component, OnInit } from '@angular/core';
import { ViewChild } from '@angular/core';
import { } from '@types/googlemaps';

@Component({
  selector: 'app-mapa',
  templateUrl: './mapa.component.html',
  styleUrls: ['./mapa.component.css']
})
export class MapaComponent implements OnInit {

  @ViewChild('gmap') gmapElement: any;
  map: google.maps.Map;

  latitude: any;
  longitude: any;

  startPos: any;
  nudge = document.getElementById('nudge');
  nudgeTimeoutId = setTimeout(this.showNudgeBanner, 5000);

  constructor() { }

  ngOnInit() {
    const mapProp = {
      center: new google.maps.LatLng(4.6015, -74.0664),
      zoom: 15,
      mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    this.map = new google.maps.Map(this.gmapElement.nativeElement, mapProp);
    // check for Geolocation support
    if (navigator.geolocation) {
      console.log('Geolocation is supported!');
      let watchId = navigator.geolocation.watchPosition(function(position) {
        this.latitude =  position.coords.latitude;
        this.longitude = position.coords.longitude;
      });
    } else {
      console.log('Geolocation is not supported for this Browser/OS.');
    }

  }

  setMapType(mapTypeId: string) {
    this.map.setMapTypeId(mapTypeId);
  }

  setCenter() {
    this.map.setCenter(new google.maps.LatLng(this.latitude, this.longitude));

    const location = new google.maps.LatLng(this.latitude, this.longitude);

    const marker = new google.maps.Marker({
      position: location,
      map: this.map,
      title: 'Got you!'
    });

    marker.addListener('click', this.simpleMarkerHandler);

    marker.addListener('click', () => {
      this.markerHandler(marker);
    });
  }

  simpleMarkerHandler() {
    alert('Simple Component\'s function...');
  }

  markerHandler(marker: google.maps.Marker) {
    alert('Marker\'s Title: ' + marker.getTitle());
  }

  showNudgeBanner() {
    this.nudge.style.display = 'block';
  }

  hideNudgeBanner() {
    this.nudge.style.display = 'none';
  }

  geoSuccess(position) {
    this.hideNudgeBanner();
    // We have the location, don't display banner
    clearTimeout(this.nudgeTimeoutId);

    // Do magic with location
    this.startPos = position;
    document.getElementById('startLat').innerHTML = this.startPos.coords.latitude;
    document.getElementById('startLon').innerHTML = this.startPos.coords.longitude;
  }

  geoError(error) {
    switch (error.code) {
      case error.TIMEOUT:
        // The user didn't accept the callout
        this.showNudgeBanner();
        break;
    }
  }
}