import { Component, OnInit } from '@angular/core';
import { AlertaService } from '../alerta.service';
import { Alerta } from './alerta';

@Component({
  selector: 'app-alerta',
  templateUrl: './alerta.component.html',
  styleUrls: ['./alerta.component.css']
})
export class AlertaComponent implements OnInit {

  alertas: Alerta[];

  constructor(private alertaService: AlertaService) { }

  ngOnInit() {
    this.getAlertas();
  }

  getAlertas(): void {
    this.alertaService.getAlertas().subscribe(alertas => this.alertas = alertas);
  }
}
