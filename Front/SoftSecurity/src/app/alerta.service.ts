import { Injectable } from '@angular/core';
import { Alerta } from './alerta';
import { ALERTAS } from './alertas';
import { Observable, of } from 'rxjs';

@Injectable({
  providedIn: 'root'
})

export class AlertaService {

  constructor() { }

  getAlertas(): Observable<Alerta[]> {
    // TODO: send the message _after_ fetching the heroes
    //this.mensajeService.add(`AlertaService: fetched alertas`);
    return of(ALERTAS);
  }

  getAlerta(cantidadAlertas: number): Observable<Alerta> {
    // TODO: send the message _after_ fetching the heroes
    //this.mensajeService.add(`HeroService: fetched hero cantidadAlertas=${cantidadAlertas}`);
    return of(ALERTAS.find(alerta => alerta.cantidadAlertas === cantidadAlertas));
  }

}
