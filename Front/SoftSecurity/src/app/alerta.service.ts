import { Injectable } from '@angular/core';
import { Alerta } from './alerta/alerta';
import { ALERTAS } from './alertas';
import { Observable, of } from 'rxjs';

@Injectable({
  providedIn: 'root'
})

export class AlertaService {

  constructor() { }

  getAlertas(): Observable<Alerta[]> {
    return of(ALERTAS);
  }

  getAlerta(id: number): Observable<Alerta> {
    return of(ALERTAS.find(alerta => alerta.id === id));
  }
}
