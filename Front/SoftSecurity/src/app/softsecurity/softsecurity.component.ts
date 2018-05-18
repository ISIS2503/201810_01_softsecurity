import { Component, OnInit } from '@angular/core';
import { Residencia } from '../residencia';
import { Alerta } from '../alerta';
import { AlertaService } from '../alerta.service';

@Component({
  selector: 'app-softsecurity',
  templateUrl: './softsecurity.component.html',
  styleUrls: ['./softsecurity.component.css']
})
export class SoftsecurityComponent implements OnInit {

  residencia: Residencia = {
    nombre: 'Residencia 1',
    numero: 1
  };

  alertas: Alerta[];

  constructor( private alertaService: AlertaService ) { }

  getAlertas(): void {
    this.alertaService.getAlertas().subscribe(alertas => this.alertas = alertas);
  }

  ngOnInit() {
    this.getAlertas();
  }

}
