import { Component, OnInit, Input} from '@angular/core';
import { Alerta } from '../alerta';
import { ActivatedRoute } from '@angular/router';
import { Location } from '@angular/common';

import { AlertaService } from '../alerta.service';

@Component({
  selector: 'app-alerta-detail',
  templateUrl: './alerta-detail.component.html',
  styleUrls: ['./alerta-detail.component.css']
})
export class AlertaDetailComponent implements OnInit {

  @Input() alerta: Alerta;

  constructor(
  private route: ActivatedRoute,
  private alertaService: AlertaService,
  private location: Location
  ) { }

  ngOnInit(): void {
    this.getAlerta();
  }

  getAlerta(): void {
    const cantidadAlertas = +this.route.snapshot.paramMap.get('cantidadAlertas');
    this.alertaService.getAlerta(cantidadAlertas).subscribe(alerta => this.alerta = alerta);
  }

  goBack(): void {
  this.location.back();
  }
}
